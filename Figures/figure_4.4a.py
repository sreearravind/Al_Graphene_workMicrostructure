import pandas as pd
import numpy as np
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

print("Columns in CSV:")
print(df.columns.tolist())

# =========================================================
# Select all numerical parameters for Pearson analysis
# =========================================================
numeric_cols = [
    "GNP (wt.%)",
    "Sintering Temperature (°C)",
    "Mean_Equivalent_grain_Diameter_um",
    "Hardness (HRB)",
    "Bulk Density (g/cm³)",
    "Extruded Density",   # keep as-is if this is how it appears in your CSV
    "Yield Strength",
    "UTS",
    "Elongation %",
    "Frictional Force (N)",
    "COF",
    "Mass Loss (g)"
]

# Optional short labels for cleaner heatmap display
label_map = {
    "GNP (wt.%)": "GNP",
    "Sintering Temperature (°C)": "Sinter Temp",
    "Mean_Equivalent_grain_Diameter_um": "Grain Size",
    "Hardness (HRB)": "Hardness",
    "Bulk Density (g/cm³)": "Bulk Density",
    "Extruded Density": "Extruded Density",
    "Yield Strength": "YS",
    "UTS": "UTS",
    "Elongation %": "Elongation",
    "Frictional Force (N)": "Friction Force",
    "COF": "COF",
    "Mass Loss (g)": "Mass Loss"
}

corr = df[numeric_cols].corr(method="pearson")

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

fig, ax = plt.subplots(figsize=(11, 9))

# Standard heatmap style
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

# Axis ticks and labels
short_labels = [label_map[col] for col in numeric_cols]
ax.set_xticks(np.arange(len(short_labels)))
ax.set_yticks(np.arange(len(short_labels)))
ax.set_xticklabels(short_labels, rotation=45, ha="right")
ax.set_yticklabels(short_labels)

# Annotate correlation values inside cells
for i in range(corr.shape[0]):
    for j in range(corr.shape[1]):
        value = corr.iloc[i, j]
        ax.text(
            j, i, f"{value:.2f}",
            ha="center", va="center",
            color="black", fontsize=9
        )

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Pearson correlation coefficient (r)", fontsize=12)

# =========================================================
# Save files
# =========================================================
tiff_file = output_dir / "Fig_4_4a_Pearson_Heatmap.tiff"
png_file = output_dir / "Fig_4_4a_Pearson_Heatmap.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print("\nPearson correlation matrix:")
print(corr.round(3))

print(f"\nTIFF saved to: {tiff_file}")
print(f"PNG saved to:  {png_file}")