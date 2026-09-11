import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# =========================================================
# File paths
# =========================================================
csv_path = r"C:\Users\HP\OneDrive\2026\Al Graphene\Supplementary_Grain_Size_hardness_tensile_desnity.csv"
output_dir = Path(r"C:\Users\HP\OneDrive\2026\Al Graphene\Figures_AlGr")
output_dir.mkdir(parents=True, exist_ok=True)

# =========================================================
# Read CSV
# =========================================================
df = pd.read_csv(csv_path, encoding="ISO-8859-1")

print("Columns in CSV:")
print(df.columns.tolist())

# =========================================================
# Column names (modify if needed)
# =========================================================
sample_col = "Sample"
ys_col = "Yield Strength"
uts_col = "UTS"
elong_col = "Elongation %"

# =========================================================
# Prepare data
# =========================================================
df = df.sort_values(by=sample_col).reset_index(drop=True)
df["SampleLabel"] = [f"S{i}" for i in df[sample_col]]

x = np.arange(len(df))
bar_width = 0.34

ys = df[ys_col]
uts = df[uts_col]
elong = df[elong_col]

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12

fig, ax1 = plt.subplots(figsize=(11.5, 7))

# =========================================================
# Bar plots (UPDATED COLORS)
# =========================================================
bars1 = ax1.bar(
    x - bar_width/2,
    ys,
    width=bar_width,
    color="skyblue",
    label="Yield Strength (MPa)"
)

bars2 = ax1.bar(
    x + bar_width/2,
    uts,
    width=bar_width,
    color="lightgreen",
    label="Ultimate Tensile Strength (MPa)"
)

ax1.set_xlabel("Sample", fontsize=13)
ax1.set_ylabel("Strength (MPa)", fontsize=13)
ax1.set_xticks(x)
ax1.set_xticklabels(df["SampleLabel"])
ax1.set_xlim(-0.6, len(df) - 0.4)

# =========================================================
# Elongation line (unchanged)
# =========================================================
ax2 = ax1.twinx()
line1 = ax2.plot(
    x,
    elong,
    color="darkred",
    marker="o",
    markersize=7,
    linewidth=2.2,
    label="Elongation (%)"
)

ax2.set_ylabel("Elongation (%)", color="darkred", fontsize=13)
ax2.tick_params(axis="y", labelcolor="darkred")

# =========================================================
# Value annotations (better spacing)
# =========================================================
for bar in bars1:
    height = bar.get_height()
    ax1.annotate(
        f"{height:.0f}",
        xy=(bar.get_x() + bar.get_width()/2, height),
        xytext=(0, 6),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8
    )

for bar in bars2:
    height = bar.get_height()
    ax1.annotate(
        f"{height:.0f}",
        xy=(bar.get_x() + bar.get_width()/2, height),
        xytext=(0, 6),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=8
    )

for xi, yi in zip(x, elong):
    ax2.annotate(
        f"{yi:.1f}",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=9,
        color="darkred"
    )

# =========================================================
# Legend moved ABOVE plot (no overlap)
# =========================================================
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    handles1 + handles2,
    labels1 + labels2,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.15),
    ncol=3,
    frameon=True,
    fontsize=11
)

# =========================================================
# Title and layout
# =========================================================
plt.title("Variation of tensile properties across Al-Gr samples", fontsize=14)

fig.tight_layout()

# =========================================================
# Save outputs
# =========================================================
tiff_file = output_dir / "Fig_4_2b_YS_UTS_Elongation.tiff"
png_file = output_dir / "Fig_4_2b_YS_UTS_Elongation.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"TIFF saved to: {tiff_file}")
print(f"PNG saved to:  {png_file}")