"""Tres figuras del preprint: pipeline, evidencia, traduccion."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

INK = "#16243B"; MUT = "#5B6B7F"; OM = "#E4572E"; NAVY = "#2C4A78"
GREY = "#9FB3C8"; LINE = "#D9DFE6"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.edgecolor": LINE, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": MUT,
                     "ytick.color": MUT})

# ---------- FIGURA 1: pipeline ----------
fig, ax = plt.subplots(figsize=(8.2, 3.1))
ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 34)

def caja(x, y, w, h, texto, fc="#FFFFFF", ec=LINE, tc=INK, fs=8.3, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6",
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w/2, y + h/2, texto, ha="center", va="center",
            fontsize=fs, color=tc, linespacing=1.35)

def flecha(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=11, color=MUT, lw=1.1))

caja(1, 22, 15, 9, "Daily prices\n(no external\nfeeds)")
caja(22, 22, 17, 9, "|corr| matrix A\n250-day window")
caja(1, 3, 15, 9, "Scheduled\nFOMC calendar\n+ placebo days")
caja(45, 25.5, 24, 7.5, "Static: tri = diag(A$^3$)\ntri-exc vs config. null", fc="#FDEDE7", ec=OM)
caja(45, 15.5, 24, 7.5, "Two-time (Omega-R):\nresp, basal, resp/basal", fc="#FDEDE7", ec=OM)
caja(45, 3, 24, 8, "Standard block:\nbeta, vols, momentum,\nreversal, past MES,\nstrength, sector", fs=7.6)
caja(76, 13, 22, 12, "Gradient boosting\n(fixed hyperparams)\n5 asset folds\npaired ablation vs\nnoise placebo", fc="#F5F7F9", fs=7.8)
flecha(16, 26.5, 22, 26.5)
flecha(39, 27.5, 45, 28.5)
flecha(39, 25, 45, 20)
flecha(16, 7.5, 44, 18)
flecha(69, 27, 76, 22)
flecha(69, 19, 76, 19)
flecha(69, 7, 76, 15)
ax.text(87, 9.5, "$\\Delta R^2$ of the Omega block\nvs the placebo floor",
        ha="center", fontsize=8.3, color=INK, style="italic")
fig.tight_layout()
fig.savefig("fig1_pipeline.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ---------- FIGURA 2: evidencia ----------
labs = ["standard\n2016-25", "standard\n2012-17", "+ sector\n2016-25",
        "+ sector\n2012-17", "max public\n2016-25", "max public\n2012-17"]
om_m = [0.034, 0.021, 0.0169, 0.0163, 0.0146, 0.0145]
om_lo = [0.027, 0.010, 0.0106, 0.0046, 0.0101, 0.0027]
om_hi = [0.042, 0.033, 0.0220, 0.0283, 0.0195, 0.0269]
pl_m = [-0.016, np.nan, -0.0179, -0.0077, -0.0146, -0.0116]
pl_lo = [-0.020, np.nan, -0.0252, -0.0129, -0.0225, -0.0206]
pl_hi = [-0.012, np.nan, -0.0119, -0.0009, -0.0089, -0.0039]

x = np.arange(6)
fig, ax = plt.subplots(figsize=(8.2, 3.4))
ax.bar(x - 0.19, om_m, 0.36, color=OM, label="Omega block")
ax.errorbar(x - 0.19, om_m,
            yerr=[np.array(om_m) - np.array(om_lo),
                  np.array(om_hi) - np.array(om_m)],
            fmt="none", ecolor=INK, elinewidth=1.1, capsize=3)
ax.bar(x + 0.19, pl_m, 0.36, color=GREY, label="noise placebo (same width)")
ax.errorbar(x + 0.19, pl_m,
            yerr=[np.nan_to_num(np.array(pl_m) - np.array(pl_lo)),
                  np.nan_to_num(np.array(pl_hi) - np.array(pl_m))],
            fmt="none", ecolor=MUT, elinewidth=1.1, capsize=3)
ax.axhline(0, color=INK, lw=1)
ax.set_xticks(x, labs, fontsize=8)
ax.set_ylabel("out-of-fold $\\Delta R^2$")
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig2_evidence.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ---------- FIGURA 3: traduccion ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.0),
                             gridspec_kw={"width_ratios": [1.5, 1]})
años = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
dr2 = [0.021, 0.145, 0.036, 0.032, -0.006, 0.036, 0.045, 0.028, 0.033]
cols = [OM if v > 0 else GREY for v in dr2]
a1.bar(años, dr2, color=cols)
a1.axhline(0, color=INK, lw=1)
a1.set_ylabel("$\\Delta R^2$ per window")
a1.set_title("a) 9 independent windows, 2016-2025", fontsize=9, loc="left")
a1.spines[["top", "right"]].set_visible(False)
a1.tick_params(axis="x", labelsize=7.5)

a2.bar(["base\nmodel", "with\nOmega", "pure\nchance"], [20.9, 22.8, 5.4],
       color=[NAVY, OM, GREY], width=0.62)
for i, v in enumerate([20.9, 22.8, 5.4]):
    a2.text(i, v + 0.6, f"{v:.1f}", ha="center", fontsize=8.5, color=INK)
a2.set_ylabel("true top-50 stress carriers caught")
a2.set_ylim(0, 27)
a2.set_title("b) practical translation", fontsize=9, loc="left")
a2.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig3_translation.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("figuras generadas")
