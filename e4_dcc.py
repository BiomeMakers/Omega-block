"""E4 con el MES condicional ESTIMADO en lugar del proxy EWMA.

QUE CIERRA. El pre-registro E4 define la quinta caracteristica de cola como un
"pronostico MES condicional tipo V-Lab (proxy EWMA lambda=0.94: rho_t * sigma_i,t
al cierre de la ventana)", y el preprint declara la rendija: el proxy es un EWMA
fijo, no un modelo estimado por maxima verosimilitud. Este script sustituye esa
columna por el MES condicional a un dia de Brownlees y Engle:

  MES_i = sigma_i,T [ rho_T * E(eps_m | eps_m < c)
                      + sqrt(1-rho_T^2) * E(xi_i | eps_m < c) ]

con sigma de un GJR-GARCH(1,1) por maxima verosimilitud, rho de un DCC(1,1)
bivariado por activo contra el mercado con correlation targeting, y las dos
esperanzas de cola estimadas de forma no parametrica sobre los residuos
estandarizados de la ventana. Todo se estima DENTRO de la ventana de 250 dias,
asi que no hay mirada al futuro.

COMO SE DEBE CITAR ESTO, y no de otra forma. La arquitectura coincide con la del
V-Lab, que estima una volatilidad asimetrica GJR-GARCH y una correlacion DCC
para cada empresa contra el indice de mercado y describe el marco GJR-DCC como
el suyo establecido para riesgo sistemico. Pero lo que aqui se calcula NO es su
LRMES ni su SRISK: el LRMES del V-Lab es a seis meses con umbral de caida del
40% y se obtiene por simulacion con residuos remuestreados, o por la forma
cerrada 1-exp(log(1-d)*beta) en la variante sin simulacion, y el SRISK combina
esa perdida con valor de mercado y deuda para dar un deficit de capital, lo que
solo tiene sentido en instituciones financieras con balance. Este panel son
acciones de todos los sectores y la ventana es de 250 dias, asi que la pieza
apropiada es el MES condicional a un dia, que es el bloque basico sobre el que
se construyen aquellas medidas.

    Redaccion correcta:  "MES condicional de Brownlees y Engle estimado con
    GJR-GARCH y DCC bivariado, la pieza sobre la que se construyen las medidas
    del V-Lab".
    Redaccion INCORRECTA: "el modelo del V-Lab", "hemos batido al V-Lab".

QUE NO REPRODUCE. E4 lleva 12 dummies de sector GICS que no estan en el panel
publico, asi que aqui no se incluyen: el nivel absoluto de dR2 NO es comparable
con el E4 publicado. Lo que si es valido es la comparacion PAREADA, porque los
dos brazos comparten absolutamente todo salvo esa columna.

PROTOCOLO, copiado del arnes publico y no tocado: ventanas de 250 dias con paso
21, HistGradientBoosting (300, prof 3, lr 0.05), 5 pliegues de activos, bootstrap
de bloques de 12 sobre el dR2 pareado, y placebo gaussiano de 5 columnas.

USO:
    python3 e4_dcc.py --prices panel.csv [--jobs N] [--max-activos N]
                      [--max-ventanas N]

Referencias:
  Brownlees, C. y R. F. Engle. SRISK: a conditional capital shortfall measure of
    systemic risk. Review of Financial Studies 30(1):48-79, 2017.
  Engle, R. F. Dynamic conditional correlation. Journal of Business and Economic
    Statistics 20(3), 2002.
  V-Lab, NYU Stern. Systemic Risk Analysis y GARCH-DCC documentation.
    vlab.stern.nyu.edu/docs/srisk y /docs/correlation/GARCH-DCC
"""
import argparse
import json
import time
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold

warnings.filterwarnings("ignore")
from arch import arch_model  # noqa: E402

VENT, PASO = 250, 21
Q_COLA = 0.05
rng = np.random.default_rng(7)


def modelo():
    return HistGradientBoostingRegressor(max_iter=300, max_depth=3,
                                         learning_rate=0.05, random_state=0)


def r2_cv(F, y):
    kf = KFold(5, shuffle=True, random_state=0)
    sr = st = 0.0
    for tr, te in kf.split(F):
        m = modelo(); m.fit(F[tr], y[tr]); p = m.predict(F[te])
        sr += ((y[te] - p) ** 2).sum(); st += ((y[te] - y[te].mean()) ** 2).sum()
    return 1 - sr / st


# ------------------------------------------------------------------ volatilidad
def gjr(serie):
    """GJR-GARCH(1,1) por maxima verosimilitud. Devuelve sigma_t y residuos
    estandarizados, en las unidades originales de la serie."""
    x = serie * 100.0
    try:
        res = arch_model(x, vol="GARCH", p=1, o=1, q=1, dist="normal",
                         mean="Constant").fit(disp="off", show_warning=False)
        sig = np.asarray(res.conditional_volatility) / 100.0
        eps = (serie - serie.mean()) / np.maximum(sig, 1e-12)
        if not np.all(np.isfinite(sig)) or sig[-1] <= 0:
            raise ValueError
    except Exception:
        sig = np.full(len(serie), serie.std())
        eps = (serie - serie.mean()) / max(serie.std(), 1e-12)
    return sig, eps


# ------------------------------------------------------------------------- DCC
def dcc_rho(em, ei):
    """DCC(1,1) bivariado con correlation targeting, dos parametros por QMLE.
    Devuelve la correlacion condicional al CIERRE de la ventana."""
    z = np.column_stack([em, ei])
    z = z / np.maximum(z.std(0), 1e-12)
    Qbar = np.corrcoef(z.T)
    if not np.all(np.isfinite(Qbar)):
        return float(np.clip(np.corrcoef(em, ei)[0, 1], -0.999, 0.999))
    T = len(z)

    def nll(p):
        a, b = p
        if a <= 0 or b <= 0 or a + b >= 0.999:
            return 1e10
        Q = Qbar.copy(); ll = 0.0
        for t in range(T):
            d = np.sqrt(np.diag(Q))
            r = Q[0, 1] / max(d[0] * d[1], 1e-12)
            r = np.clip(r, -0.9999, 0.9999)
            det = 1 - r * r
            u, v = z[t]
            ll += np.log(det) + (u * u + v * v - 2 * r * u * v) / det
            zz = np.outer(z[t], z[t])
            Q = (1 - a - b) * Qbar + a * zz + b * Q
        return 0.5 * ll

    best = None
    for x0 in ((0.02, 0.95), (0.05, 0.90)):
        try:
            r_ = minimize(nll, x0, method="Nelder-Mead",
                          options={"maxiter": 120, "xatol": 1e-3, "fatol": 1e-2})
            if best is None or r_.fun < best.fun:
                best = r_
        except Exception:
            pass
    a, b = (best.x if best is not None and best.fun < 1e9 else (0.02, 0.95))
    a, b = max(a, 1e-4), max(b, 1e-4)
    if a + b >= 0.999:
        a, b = 0.02, 0.95
    Q = Qbar.copy()
    for t in range(T):
        Q = (1 - a - b) * Qbar + a * np.outer(z[t], z[t]) + b * Q
    d = np.sqrt(np.diag(Q))
    return float(np.clip(Q[0, 1] / max(d[0] * d[1], 1e-12), -0.999, 0.999))


def _mes_uno(col, eps_m, cola, E_em):
    sig_i, eps_i = gjr(col)
    rho = dcc_rho(eps_m, eps_i)
    q = np.sqrt(max(1 - rho * rho, 1e-9))
    xi = (eps_i - rho * eps_m) / q
    return sig_i[-1] * (rho * E_em + q * xi[cola].mean())


def mes_dcc(W, mw, n_jobs=-1):
    """MES condicional de Brownlees-Engle para cada activo, al cierre de W.
    El bucle por activo es vergonzosamente paralelo: cada uno es un GJR mas un
    DCC bivariado contra el mismo mercado."""
    sig_m, eps_m = gjr(mw)
    cola = eps_m < np.quantile(eps_m, Q_COLA)
    if cola.sum() < 3:
        cola = eps_m <= np.quantile(eps_m, 0.1)
    E_em = eps_m[cola].mean()
    if n_jobs == 1:
        return np.array([_mes_uno(W[:, i], eps_m, cola, E_em)
                         for i in range(W.shape[1])])
    from joblib import Parallel, delayed
    return np.array(Parallel(n_jobs=n_jobs, prefer="processes")(
        delayed(_mes_uno)(W[:, i], eps_m, cola, E_em) for i in range(W.shape[1])))


def mes_ewma(W, mw, lam=0.94):
    """El proxy del pre-registro E4: rho_t * sigma_i,t con EWMA lambda=0.94."""
    T, n = W.shape
    w = lam ** np.arange(T - 1, -1, -1) * (1 - lam)
    w = w / w.sum()
    dm = mw - (w * mw).sum()
    var_m = (w * dm * dm).sum()
    D = W - (w[:, None] * W).sum(0)
    var_i = (w[:, None] * D * D).sum(0)
    cov = (w[:, None] * D * dm[:, None]).sum(0)
    sig_i = np.sqrt(np.maximum(var_i, 1e-18))
    rho = cov / np.maximum(sig_i * np.sqrt(max(var_m, 1e-18)), 1e-18)
    return np.clip(rho, -1, 1) * sig_i


# --------------------------------------------------------------- caracteristicas
def cola_features(W, mw, quinta):
    """beta bajista, cosimetria, cocurtosis, semidesviacion, y la quinta."""
    n = W.shape[1]
    neg = mw < 0
    mm, sm = mw.mean(), mw.std()
    dm = mw - mm
    Wm = W.mean(0); Ws = W.std(0)
    d = W - Wm
    beta_b = np.array([np.cov(W[neg, i], mw[neg])[0, 1] for i in range(n)]) / mw[neg].var()
    cosk = (d * dm[:, None] ** 2).mean(0) / np.maximum(Ws * sm ** 2, 1e-18)
    cokur = (d * dm[:, None] ** 3).mean(0) / np.maximum(Ws * sm ** 3, 1e-18)
    semi = np.array([W[W[:, i] < 0, i].std() if (W[:, i] < 0).sum() > 2 else Ws[i]
                     for i in range(n)])
    return np.column_stack([beta_b, cosk, cokur, semi, quinta])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", required=True)
    ap.add_argument("--max-activos", type=int, default=0)
    ap.add_argument("--max-ventanas", type=int, default=0)
    ap.add_argument("--out", default="e4_dcc_resultado.json")
    ap.add_argument("--jobs", type=int, default=-1,
                    help="nucleos para el bucle DCC (-1 = todos)")
    a = ap.parse_args()

    P = pd.read_csv(a.prices, parse_dates=[0], index_col=0).sort_index()
    P = P.loc[:, P.notna().mean() >= 0.95]
    R = np.log(P).diff().iloc[1:].fillna(0.0)
    if a.max_activos:
        R = R.iloc[:, :a.max_activos]
    X, n = R.values, R.shape[1]
    inis = list(range(VENT, len(R) - VENT + 1, PASO))
    if a.max_ventanas:
        inis = inis[:a.max_ventanas]
    print(f"panel: {len(R)} dias, {n} activos, {len(inis)} ventanas", flush=True)

    d_ew, d_dc, d_pl_ew, d_pl_dc = [], [], [], []
    t_ini = time.time()
    for k, t in enumerate(inis, 1):
        W, F = X[t - VENT:t], X[t:t + VENT]
        mw, mf = W.mean(1), F.mean(1)
        # los 7 estandar del arnes
        beta = np.array([np.cov(W[:, i], mw)[0, 1] for i in range(n)]) / mw.var()
        mes_hist = W[mw <= np.quantile(mw, 0.05)].mean(0)
        A = np.abs(np.corrcoef(W.T)); np.fill_diagonal(A, 0)
        s = A.sum(1)
        est = np.column_stack([beta, W[-21:].std(0), W.std(0),
                               W[:-21].sum(0), W[-21:].sum(0), mes_hist, s])
        # bloque Omega estatico
        tri = ((A @ A) * A).sum(1)
        E = s ** 2 * (s ** 2).sum() ** 2 / (s.sum() ** 3)
        om = np.column_stack([tri, (tri - E) / np.maximum(E, 1e-12)])
        y = F[mf <= np.quantile(mf, 0.05)].mean(0)
        ruido = rng.standard_normal((n, 5))

        for etiqueta, quinta, dd, dp in (
                ("ewma", mes_ewma(W, mw), d_ew, d_pl_ew),
                ("dcc", mes_dcc(W, mw, a.jobs), d_dc, d_pl_dc)):
            base = np.column_stack([est, cola_features(W, mw, quinta)])
            rb = r2_cv(base, y)
            dd.append(r2_cv(np.column_stack([base, om]), y) - rb)
            dp.append(r2_cv(np.column_stack([base, ruido]), y) - rb)
        print(f"  ventana {k}/{len(inis)}  ewma {d_ew[-1]:+.4f}  "
              f"dcc {d_dc[-1]:+.4f}  ({time.time()-t_ini:.0f}s)", flush=True)

    def ic(v, blq=12, B=2000):
        v = np.asarray(v); nb = int(np.ceil(len(v) / blq)); out = np.empty(B)
        for b in range(B):
            s0 = rng.integers(0, max(len(v) - blq + 1, 1), nb)
            idx = np.concatenate([np.arange(x, x + blq) for x in s0])[:len(v)]
            out[b] = v[np.clip(idx, 0, len(v) - 1)].mean()
        return np.percentile(out, [2.5, 97.5])

    res = {}
    print()
    for nom, dd, dp in (("proxy EWMA lambda=0.94 (E4 publicado)", d_ew, d_pl_ew),
                        ("MES condicional GJR-DCC (Brownlees-Engle)", d_dc, d_pl_dc)):
        i1, i2 = ic(dd), ic(dp)
        ok = i1[0] > 0 and i1[0] > i2[1]
        print(f"{nom:42} dR2 Omega {np.mean(dd):+.4f} [{i1[0]:+.4f}, {i1[1]:+.4f}]"
              f"   placebo {np.mean(dp):+.4f} [{i2[0]:+.4f}, {i2[1]:+.4f}]"
              f"   {'PASS' if ok else 'FAIL'}")
        res[nom] = {"dR2": float(np.mean(dd)), "ci": [float(i1[0]), float(i1[1])],
                    "placebo": float(np.mean(dp)), "acceptance": "PASS" if ok else "FAIL"}
    dif = np.array(d_dc) - np.array(d_ew)
    print(f"\ndiferencia pareada (DCC - EWMA): {dif.mean():+.4f}  "
          f"ventanas a favor del DCC {int((dif>0).sum())}/{len(dif)}")
    res["pareado_dcc_menos_ewma"] = {"media": float(dif.mean()),
                                     "a_favor": int((dif > 0).sum()),
                                     "n": int(len(dif))}
    json.dump(res, open(a.out, "w"), indent=2)


if __name__ == "__main__":
    main()
