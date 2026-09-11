from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
hardness_file = HERE / "hardness_data.csv"
comment10_file = HERE.parent / "Revision_Comment10" / "comment10_factor_comparison_data.csv"

hard = pd.read_csv(hardness_file)
base = pd.read_csv(comment10_file)

rep_cols = [f"H{i}" for i in range(1, 10)]
hard["Hardness_mean_calc"] = hard[rep_cols].mean(axis=1)
hard["Hardness_SD_calc"] = hard[rep_cols].std(axis=1, ddof=1)
hard["Hardness_SE_calc"] = hard["Hardness_SD_calc"] / math.sqrt(9)
hard["Hardness_CV_pct"] = 100 * hard["Hardness_SD_calc"] / hard["Hardness_mean_calc"]

summary = hard[[
    "Sample", "GNP_wt_pct", "Sintering_Temperature_C",
    "Hardness_mean_calc", "Hardness_SD_calc", "Hardness_SE_calc", "Hardness_CV_pct"
]].copy()
summary.to_csv(HERE / "hardness_summary_comment7.csv", index=False)

# Match order to the condition-level comparison dataset.
df = base.merge(summary, on=["Sample", "GNP_wt_pct", "Sintering_Temperature_C"], how="left")

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.labelsize": 15,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
})

# ------------------------------------------------------------------
# Revised Figure 5: hardness mean +/- SD (n=9 spatial indentations)
# plus extruded density.
# ------------------------------------------------------------------
x = np.arange(len(df))
fig, ax1 = plt.subplots(figsize=(11.8, 7.2))

ax1.errorbar(
    x, df["Hardness_mean_calc"], yerr=df["Hardness_SD_calc"],
    marker="o", markersize=7.5, linewidth=2.1,
    capsize=5, elinewidth=1.4,
    label="Rockwell hardness (mean ± SD, n = 9)"
)
ax1.set_xlabel("Processing condition")
ax1.set_ylabel("Rockwell hardness (HRB)", fontweight="bold")
ax1.set_xticks(x, df["Sample"])
ax1.set_xlim(-0.45, len(df)-0.55)
ax1.grid(axis="y", alpha=0.22)

for xi, yi in zip(x, df["Hardness_mean_calc"]):
    ax1.annotate(f"{yi:.2f}", (xi, yi), xytext=(0, 10),
                 textcoords="offset points", ha="center",
                 fontsize=10.5, fontweight="bold")

ax2 = ax1.twinx()
ax2.plot(
    x, df["Extruded_Density_g_cm3"],
    marker="s", linestyle="--", markersize=6.5, linewidth=1.9,
    label="Extruded density"
)
ax2.set_ylabel("Extruded density (g/cm³)", fontweight="bold")

for xi, yi in zip(x, df["Extruded_Density_g_cm3"]):
    ax2.annotate(f"{yi:.3f}", (xi, yi), xytext=(0, -17),
                 textcoords="offset points", ha="center", fontsize=9.5)

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc="upper center", bbox_to_anchor=(0.5, 1.12),
           ncol=2, frameon=True)
fig.tight_layout()
fig.savefig(HERE / "Figure_5_Hardness_Density_with_SD.png", dpi=600, bbox_inches="tight")
fig.savefig(HERE / "Figure_5_Hardness_Density_with_SD.tiff", dpi=600, bbox_inches="tight",
            pil_kwargs={"compression": "tiff_lzw"})
fig.savefig(HERE / "Figure_5_Hardness_Density_with_SD.svg", bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------
# Revised Comment-10 interaction plot: panel (c) now carries the same
# hardness SD error bars for consistency with Figure 5.
# ------------------------------------------------------------------
responses = [
    ("Extruded_Density_g_cm3", "Extruded density (g/cm³)", "(a) Extruded density"),
    ("Mean_Equivalent_Grain_Diameter_um", "Mean equivalent grain diameter (µm)", "(b) Grain size"),
    ("Hardness_mean_calc", "Rockwell hardness (HRB)", "(c) Rockwell hardness"),
    ("UTS_MPa", "Ultimate tensile strength (MPa)", "(d) Ultimate tensile strength"),
    ("COF", "Coefficient of friction", "(e) Coefficient of friction"),
    ("Mass_Loss_g", "Mass loss (g)", "(f) Mass loss"),
]

fig, axes = plt.subplots(2, 3, figsize=(12, 7.5), sharex=True)
axes = axes.ravel()
markers = ["o", "s", "^"]

for ax, (col, ylabel, title) in zip(axes, responses):
    for marker, temp in zip(markers, [500, 550, 600]):
        sub = df[df["Sintering_Temperature_C"] == temp].sort_values("GNP_wt_pct")
        if col == "Hardness_mean_calc":
            ax.errorbar(sub["GNP_wt_pct"], sub[col], yerr=sub["Hardness_SD_calc"],
                        marker=marker, linewidth=1.8, markersize=5.5,
                        capsize=3.5, elinewidth=1.1, label=f"{temp} °C")
        else:
            ax.plot(sub["GNP_wt_pct"], sub[col], marker=marker,
                    linewidth=1.8, markersize=5.5, label=f"{temp} °C")
        
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_xticks([0, 2, 3, 4])
    ax.grid(True, alpha=0.22)

for ax in axes[3:]:
    ax.set_xlabel("GNP content (wt.%)")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.995))
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(HERE / "Figure_12_Comparative_with_Hardness_SD.png", dpi=600, bbox_inches="tight")
fig.savefig(HERE / "Figure_12_Comparative_with_Hardness_SD.tiff", dpi=600, bbox_inches="tight",
            pil_kwargs={"compression": "tiff_lzw"})
fig.savefig(HERE / "Figure_12_Comparative_with_Hardness_SD.svg", bbox_inches="tight")
plt.close(fig)

print(summary.to_string(index=False))
