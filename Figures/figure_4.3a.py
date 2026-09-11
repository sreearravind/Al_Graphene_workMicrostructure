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
# Column names (update if needed)
# =========================================================
sample_col = "Sample"
cof_col = "COF"
mass_col = "Mass Loss (g)"

# =========================================================
# Prepare data
# =========================================================
df = df.sort_values(by=sample_col).reset_index(drop=True)
df["SampleLabel"] = [f"S{i}" for i in df[sample_col]]

x = np.arange(len(df))
cof = df[cof_col]
mass = df[mass_col]

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12

fig, ax1 = plt.subplots(figsize=(11, 6.8))

# =========================================================
# COF plot (Left axis)
# =========================================================
line1 = ax1.plot(
    x,
    cof,
    color="darkblue",
    marker="o",
    markersize=7,
    linewidth=2.2,
    label="COF"
)

ax1.set_xlabel("Sample", fontsize=13)
ax1.set_ylabel("Coefficient of Friction (COF)", color="darkblue", fontsize=13)
ax1.tick_params(axis="y", labelcolor="darkblue")
ax1.set_xticks(x)
ax1.set_xticklabels(df["SampleLabel"])
ax1.set_xlim(-0.4, len(df) - 0.6)

# =========================================================
# Mass loss plot (Right axis)
# =========================================================
ax2 = ax1.twinx()

line2 = ax2.plot(
    x,
    mass,
    color="darkgreen",
    marker="s",
    markersize=7,
    linewidth=2.2,
    label="Mass Loss (g)"
)

ax2.set_ylabel("Mass Loss (g)", color="darkgreen", fontsize=13)
ax2.tick_params(axis="y", labelcolor="darkgreen")

# =========================================================
# Value annotations (optimized spacing)
# =========================================================
for xi, yi in zip(x, cof):
    ax1.annotate(
        f"{yi:.3f}",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8,
        color="darkblue"
    )

for xi, yi in zip(x, mass):
    ax2.annotate(
        f"{yi:.4f}",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, -14),
        ha="center",
        fontsize=8,
        color="darkgreen"
    )

# =========================================================
# Legend (top center)
# =========================================================
lines = line1 + line2
labels = [l.get_label() for l in lines]

ax1.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.15),
    ncol=2,
    frameon=True,
    fontsize=11
)

# =========================================================
# Title and layout
# =========================================================
plt.title("Variation of coefficient of friction and mass loss in  Al Gr samples", fontsize=14)

fig.tight_layout()

# =========================================================
# Save outputs
# =========================================================
tiff_file = output_dir / "Fig_4_3a_COF_MassLoss.tiff"
png_file = output_dir / "Fig_4_3a_COF_MassLoss.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"TIFF saved to: {tiff_file}")
print(f"PNG saved to:  {png_file}")