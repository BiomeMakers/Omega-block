"""Figura 4: el proceso de verificacion y sus piezas."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK="#16243B"; MUT="#5B6B7F"; OM="#E4572E"; LINE="#D9DFE6"; PAP="#F5F7F9"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"text.color":INK})
fig, ax = plt.subplots(figsize=(8.2, 3.6))
ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,40)
def caja(x,y,w,h,t,fc="#FFF",ec=LINE,fs=8.0,tc=INK,lw=1.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.6",fc=fc,ec=ec,lw=lw))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,color=tc,linespacing=1.4)
def fl(x1,y1,x2,y2,txt=None):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=11,color=MUT,lw=1.1))
    if txt: ax.text((x1+x2)/2,(y1+y2)/2+1.6,txt,ha="center",fontsize=7.2,color=MUT)
# columna publica
ax.text(11,38,"PUBLIC RELEASE",fontsize=8.5,ha="center",color=MUT)
caja(1,27,20,8,"Paper + formulas\npre-registrations\nresult logs")
caja(1,16,20,8,"Acceptance harness\n(open source)")
caja(1,5,20,8,"Feature files +\nSHA-256 time-lock\ncommitments")
# columna evaluador
ax.text(50,38,"EVALUATOR SIDE (their environment, their data)",fontsize=8.5,ha="center",color=MUT)
caja(33,25.5,30,9.5,"Step 1. Signal trial\nvalues-only file (date, ticker, 5 cols);\nno formulas disclosed, no code of ours runs",fc=PAP)
caja(33,13.5,30,9,"Step 2. Own-data ablation\ntheir universe, their baseline,\ntheir event calendar",fc=PAP)
caja(33,2,30,9,"Step 3 (optional). Forward audit\ntime-locked values vs realized\noutcomes next quarter",fc=PAP)
# gate
caja(70,13.5,28,13,"Acceptance gate\n$\\Delta R^2$ CI95 excludes 0\nAND clears the\nnoise-placebo floor",fc="#FDEDE7",ec=OM,fs=8.2)
ax.text(84,9.5,"PASS: license talks\nFAIL: engagement ends",ha="center",fontsize=7.6,color=MUT)
fl(21,30.5,33,29.5); fl(21,20,33,18); fl(21,9,33,6.5)
fl(63,30,72,26.5); fl(63,18,70,19); fl(63,6.5,72,13.5)
fig.tight_layout(); fig.savefig("fig4_process.png",dpi=200,bbox_inches="tight")
print("fig4 ok")
