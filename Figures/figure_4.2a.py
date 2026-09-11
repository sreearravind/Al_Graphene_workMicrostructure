import pandas as pd
import matplotlib.pyplot as plt
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

# =========================================================
# Column check and cleanup
# =========================================================
print("Columns in CSV:")
print(df.columns.tolist())

# Update these only if your CSV column names differ
sample_col = "Sample"
hardness_col = "Hardness (HRB)"

# Try to auto-detect extruded density column
density_candidates = [col for col in df.columns if "Extruded Density" in col]
if not density_candidates:
    raise ValueError("Could not find the 'Extruded Density' column in the CSV.")
density_col = density_candidates[0]

# =========================================================
# Prepare plotting data
# =========================================================
df = df.sort_values(by=sample_col).reset_index(drop=True)
df["SampleLabel"] = [f"S{i}" for i in df[sample_col]]

x = range(len(df))
hardness = df[hardness_col]
density = df[density_col]

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12

fig, ax1 = plt.subplots(figsize=(10.5, 6.5))

# Hardness plot - dark blue
line1 = ax1.plot(
    x, hardness,
    color="darkblue",
    marker="o",
    markersize=7,
    linewidth=2.2,
    label="Hardness (HRB)"
)

ax1.set_xlabel("Sample", fontsize=13)
ax1.set_ylabel("Hardness (HRB)", color="darkblue", fontsize=13)
ax1.tick_params(axis="y", labelcolor="darkblue")
ax1.set_xticks(list(x))
ax1.set_xticklabels(df["SampleLabel"])
ax1.set_xlim(-0.3, len(df) - 0.7)

# Density plot - dark green
ax2 = ax1.twinx()
line2 = ax2.plot(
    x, density,
    color="darkgreen",
    marker="s",
    markersize=7,
    linewidth=2.2,
    label="Extruded Density (g/cm³)"
)

ax2.set_ylabel("Extruded Density (g/cm³)", color="darkgreen", fontsize=13)
ax2.tick_params(axis="y", labelcolor="darkgreen")

# =========================================================
# Value annotations
# =========================================================
for xi, yi in zip(x, hardness):
    ax1.annotate(
        f"{yi:.2f}",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=9,
        color="darkblue"
    )

for xi, yi in zip(x, density):
    ax2.annotate(
        f"{yi:.3f}",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, -14),
        ha="center",
        fontsize=9,
        color="darkgreen"
    )

# =========================================================
# Legend at top right
# =========================================================
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", frameon=True, fontsize=11)

# =========================================================
# Final formatting
# =========================================================
plt.title("Variation of hardness and extruded density across samples", fontsize=14)
fig.tight_layout()

# =========================================================
# Save outputs
# =========================================================
tiff_file = output_dir / "Fig_4_2a_Hardness_Extruded_Density.tiff"
png_file = output_dir / "Fig_4_2a_Hardness_Extruded_Density.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"TIFF saved to: {tiff_file}")
print(f"PNG saved to:  {png_file}")