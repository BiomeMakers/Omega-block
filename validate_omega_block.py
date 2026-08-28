"""Validation harness for the Omega feature block.
Run it on YOUR prices. Acceptance test: the Omega block must beat a
same-width noise placebo on out-of-fold dR2 with a block-bootstrap CI
excluding zero. If it does not on your data, do not license it.

Usage:
  python validate_omega_block.py --prices prices.csv [--events events.csv]
  python validate_omega_block.py --prices prices.csv --features block.csv
  With --features, the Omega block is read from an EXTERNAL file instead of
  being computed: columns date,ticker,f1..fK, one row per rebalance date and
  asset. This is the signal-trial mode: the vendor tests the numbers without
  ever seeing the formulas.
  prices.csv: wide CSV, first column Date, one column per asset (close).
  events.csv (optional): one date per line (macro announcement days).
          If omitted, the two-time features are skipped and only the
          static triadic features are tested.
Fixed protocol (do not tune): 250d windows, HistGradientBoosting
(300 trees, depth 3, lr 0.05), 5 asset folds, overlapping windows step 21,
block bootstrap (12) on paired dR2, plus a 5-column Gaussian placebo.
"""
import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold

VENT, PASO = 250, 21
rng = np.random.default_rng(7)

def modelo():
    return HistGradientBoostingRegressor(max_iter=300, max_depth=3,
                                         learning_rate=0.05, random_state=0)

def r2_cv(F, y):
    kf = KFold(5, shuffle=True, random_state=0)
    sr = st = 0.0
    for tr, te in kf.split(F):
        m = modelo(); m.fit(F[tr], y[tr]); p = m.predict(F[te])
        sr += ((y[te]-p)**2).sum(); st += ((y[te]-y[te].mean())**2).sum()
    return 1 - sr/st

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", required=True)
    ap.add_argument("--events", default=None)
    ap.add_argument("--features", default=None,
                    help="external feature file: date,ticker,f1..fK")
    ap.add_argument("--receipt", default=None, metavar="FILE.json",
                    help="write an aggregate-only, shareable result receipt "
                         "(no tickers, no returns, no baseline composition)")
    ap.add_argument("--label", default="undisclosed",
                    help="optional coarse label for the receipt, e.g. "
                         "'US equities' or 'EU credit'; free text, your choice")
    a = ap.parse_args()
    P = pd.read_csv(a.prices, parse_dates=[0], index_col=0).sort_index()
    P = P.loc[:, P.notna().mean() >= 0.95]
    R = np.log(P).diff().iloc[1:].fillna(0.0)
    X, fechas, n = R.values, R.index, R.shape[1]
    ev = []
    if a.events:
        dts = pd.to_datetime(pd.read_csv(a.events, header=None)[0])
        ev = sorted({fechas.searchsorted(d) for d in dts
                     if fechas[0] <= d <= fechas[-1]})
        ev = [j for j in ev if 21 <= j < len(fechas)-20]
    lejos = np.ones(len(fechas), bool)
    for j in ev: lejos[max(0, j-10):j+11] = False
    lejos[:21] = False; lejos[-20:] = False
    pl = sorted(rng.choice(np.where(lejos)[0], size=max(len(ev), 1),
                           replace=False)) if len(ev) else []

    def resp(j):
        Apre = np.abs(np.corrcoef(X[j-21:j-1].T)); np.fill_diagonal(Apre, 0)
        Apos = np.abs(np.corrcoef(X[j+1:j+21].T)); np.fill_diagonal(Apos, 0)
        num = (Apre*Apos).sum(1)
        den = np.linalg.norm(Apre, axis=1)*np.linalg.norm(Apos, axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            return 1 - num/den
    r_ev = {j: resp(j) for j in ev}; r_pl = {j: resp(j) for j in pl}

    def rell(v):
        m = np.nanmedian(v); return np.where(np.isfinite(v), v,
                                             m if np.isfinite(m) else 0.0)

    def ventana(t):
        W = X[t-VENT:t]; F = X[t:t+VENT]
        mw, mf = W.mean(1), F.mean(1)
        beta = np.array([np.cov(W[:, i], mw)[0, 1] for i in range(n)])/mw.var()
        mes_p = W[mw <= np.quantile(mw, 0.05)].mean(0)
        A = np.abs(np.corrcoef(W.T)); np.fill_diagonal(A, 0)
        s = A.sum(1); A2 = A@A; tri = (A2*A).sum(1)
        E = s**2*(s**2).sum()**2/(s.sum()**3)
        base = np.column_stack([beta, W[-21:].std(0), W.std(0),
                                W[:-21].sum(0), W[-21:].sum(0), mes_p, s])
        om = [tri, (tri-E)/np.maximum(E, 1e-12)]
        if len(ev):
            evs = [j for j in ev if t-VENT <= j-21 and j+20 <= t-1] or \
                  [j for j in ev if t-500 <= j-21 and j+20 <= t-1]
            pls = [j for j in pl if t-VENT <= j-21 and j+20 <= t-1] or \
                  [j for j in pl if t-500 <= j-21 and j+20 <= t-1]
            if len(evs) >= 3 and len(pls) >= 3:
                rv = rell(np.nanmedian([r_ev[j] for j in evs], axis=0))
                bs = rell(np.nanmedian([r_pl[j] for j in pls], axis=0))
                om += [rv, bs, rell(np.where(bs > 1e-9, rv/np.maximum(bs, 1e-9),
                                             np.nan))]
        om = np.column_stack(om)
        y = F[mf <= np.quantile(mf, 0.05)].mean(0)
        return base, om, y

    FX = None
    if a.features:
        F = pd.read_csv(a.features, parse_dates=[0])
        F.columns = ["date", "ticker"] + list(F.columns[2:])
        F = F.set_index(["date", "ticker"]).sort_index()
        fcols = list(F.columns)
        def bloque_externo(fin):
            dts = F.index.get_level_values(0).unique()
            prev = dts[dts <= fin]
            if len(prev) == 0 or (fin - prev[-1]).days > 7:
                return None
            sub = F.loc[prev[-1]]
            M = sub.reindex(R.columns)[fcols].values.astype(float)
            med = np.nanmedian(M, axis=0)
            return np.where(np.isfinite(M), M, med)
        FX = bloque_externo

    inis = list(range(VENT, len(fechas)-VENT+1, PASO))
    d_om, d_pl = [], []
    for t in inis:
        b, o, y = ventana(t)
        if FX is not None:
            oe = FX(fechas[t-1])
            if oe is None:
                continue
            o = oe
        rb = r2_cv(b, y)
        d_om.append(r2_cv(np.column_stack([b, o]), y) - rb)
        d_pl.append(r2_cv(np.column_stack([b, rng.standard_normal((n, 5))]), y) - rb)
    d_om, d_pl = np.array(d_om), np.array(d_pl)

    def ic(v, blq=12, B=2000):
        nb = int(np.ceil(len(v)/blq)); out = np.empty(B)
        for b in range(B):
            s0 = rng.integers(0, len(v)-blq+1, nb)
            idx = np.concatenate([np.arange(x, x+blq) for x in s0])[:len(v)]
            out[b] = v[idx].mean()
        return np.percentile(out, [2.5, 97.5])

    io, ip = ic(d_om), ic(d_pl)
    print(f"windows: {len(d_om)} | assets: {n} | events used: {len(ev)}")
    print(f"dR2 Omega   {d_om.mean():+.4f}  CI95 [{io[0]:+.4f}, {io[1]:+.4f}]")
    print(f"dR2 placebo {d_pl.mean():+.4f}  CI95 [{ip[0]:+.4f}, {ip[1]:+.4f}]")
    ok = io[0] > 0 and io[0] > ip[1]
    print("ACCEPTANCE:", "PASS" if ok else "FAIL",
          "(Omega CI must exclude 0 and clear the placebo ceiling)")
    if a.receipt:
        import json, hashlib, datetime
        cuerpo = {
            "tool": "validate_omega_block v1.1",
            "date_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
            "label": a.label,
            "mode": "signal_trial" if a.features else "self_computed",
            "n_assets_bucket": ("<100" if n < 100 else "100-500"
                                 if n <= 500 else ">500"),
            "n_windows": int(len(d_om)),
            "n_events": int(len(ev)),
            "dR2_omega": {"mean": round(float(d_om.mean()), 4),
                          "ci95": [round(float(io[0]), 4),
                                   round(float(io[1]), 4)]},
            "dR2_placebo": {"mean": round(float(d_pl.mean()), 4),
                            "ci95": [round(float(ip[0]), 4),
                                     round(float(ip[1]), 4)]},
            "acceptance": "PASS" if ok else "FAIL",
        }
        cuerpo["receipt_sha256"] = hashlib.sha256(
            json.dumps(cuerpo, sort_keys=True).encode()).hexdigest()
        with open(a.receipt, "w") as fh:
            json.dump(cuerpo, fh, indent=2)
        print(f"\nReceipt written to {a.receipt}. It contains ONLY the "
              "aggregates above: no tickers, no returns, no dates beyond "
              "today, no baseline composition. Review it, then share it "
              "with us if you wish (see REGISTRY.md).")

if __name__ == "__main__":
    main()
