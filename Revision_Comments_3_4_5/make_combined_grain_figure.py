from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Revision_Comments_3_4_5" / "output"

grains = pd.read_csv(OUT / "grain_level_multifield_100x.csv")
summary = pd.read_csv(OUT / "condition_level_grain_summary_100x.csv")
samples = [f"S{i}" for i in range(1, 13)]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

fig = plt.figure(figsize=(13, 9))
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1], hspace=0.38, wspace=0.32)

# (a) Grain-size distributions across the twelve conditions.
ax = fig.add_subplot(gs[0, :])
data = [grains.loc[grains["Sample"] == s, "equivalent_diameter_um"].astype(float).to_numpy() for s in samples]
ax.boxplot(data, tick_labels=samples, showfliers=True, medianprops={"linewidth": 1.8})
ax.set_xlabel("Processing condition", fontweight="bold")
ax.set_ylabel("Equivalent grain diameter (µm)", fontweight="bold")
ax.set_title("(a) Grain-size distributions from three 100× fields per condition", loc="left", fontweight="bold")
ax.grid(axis="y", alpha=0.22)

x = summary["Pooled_Mean_ECD_um"].to_numpy(float)
responses = [
    ("Hardness_HRB", "Rockwell hardness (HRB)", "(b)"),
    ("UTS_MPa", "Ultimate tensile strength (MPa)", "(c)"),
    ("Elongation_pct", "Elongation (%)", "(d)"),
]
for col, ylabel, panel in responses:
    ax = fig.add_subplot(gs[1, responses.index((col, ylabel, panel))])
    y = summary[col].to_numpy(float)
    ax.scatter(x, y, s=55, edgecolors="black", linewidths=0.6)
    coef = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 200)
    ax.plot(xx, np.polyval(coef, xx), linestyle="--", linewidth=1.7)
    r = np.corrcoef(x, y)[0, 1]
    for _, row in summary.iterrows():
        ax.annotate(row["Sample"], (row["Pooled_Mean_ECD_um"], row[col]), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Mean equivalent grain diameter (µm)", fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_title(f"{panel} r = {r:.3f}", loc="left", fontweight="bold")
    ax.grid(alpha=0.22)

fig.tight_layout()
fig.savefig(OUT / "Figure_Grain_Distributions_and_Mechanical_Correlations.png", dpi=600, bbox_inches="tight")
fig.savefig(OUT / "Figure_Grain_Distributions_and_Mechanical_Correlations.tiff", dpi=600, bbox_inches="tight", pil_kwargs={"compression":"tiff_lzw"})
plt.close(fig)
