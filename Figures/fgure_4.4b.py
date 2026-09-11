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
df.columns = df.columns.str.strip()

print("Columns in CSV:")
print(df.columns.tolist())

# =========================================================
# Numerical columns
# =========================================================
numeric_cols = [
    "GNP (wt.%)",
    "Sintering Temperature (°C)",
    "Mean_Equivalent_grain_Diameter_um",
    "Hardness (HRB)",
    "Bulk Density (g/cm³)",
    "Extruded Density",
    "Yield Strength",
    "UTS",
    "Elongation %",
    "Frictional Force (N)",
    "COF",
    "Mass Loss (g)"
]

# =========================================================
# Short labels
# =========================================================
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

# =========================================================
# Pearson correlation matrix
# =========================================================
corr = df[numeric_cols].corr(method="pearson")

# =========================================================
# Targets
# =========================================================
target_uts = "UTS"
target_wear = "Mass Loss (g)"

uts_corr = corr[target_uts].drop(target_uts)
wear_corr = corr[target_wear].drop(target_wear)

# =========================================================
# Use only common parameters present in both series
# =========================================================
common_params = [param for param in uts_corr.index if param in wear_corr.index]

uts_corr_common = uts_corr[common_params]
wear_corr_common = wear_corr[common_params]

# Rank by absolute correlation magnitude with UTS
ranking_order = uts_corr_common.abs().sort_values(ascending=False).index

uts_values = uts_corr_common[ranking_order]
wear_values = wear_corr_common[ranking_order]

short_labels = [label_map[col] for col in ranking_order]

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

fig, ax = plt.subplots(figsize=(12.5, 7.5))

x = np.arange(len(ranking_order))
width = 0.36

# =========================================================
# Bars
# =========================================================
bars1 = ax.bar(
    x - width/2,
    uts_values,
    width,
    label="Correlation with UTS",
    color="skyblue",
    edgecolor="black",
    linewidth=0.8
)

bars2 = ax.bar(
    x + width/2,
    wear_values,
    width,
    label="Correlation with Mass Loss",
    color="lightgreen",
    edgecolor="black",
    linewidth=0.8
)

# =========================================================
# Annotate values
# =========================================================
def annotate_bars(bars):
    for bar in bars:
        height = bar.get_height()
        if height >= 0:
            y_offset = 4
            va = "bottom"
        else:
            y_offset = -12
            va = "top"

        ax.annotate(
            f"{height:.2f}",
            xy=(bar.get_x() + bar.get_width()/2, height),
            xytext=(0, y_offset),
            textcoords="offset points",
            ha="center",
            va=va,
            fontsize=8
        )

annotate_bars(bars1)
annotate_bars(bars2)

# =========================================================
# Axes formatting
# =========================================================
ax.set_xticks(x)
ax.set_xticklabels(short_labels, rotation=45, ha="right")
ax.set_ylabel("Pearson Correlation Coefficient (r)", fontsize=12)
ax.set_xlabel("Parameters", fontsize=12)
ax.set_title(
    "Fig. 4.4b. Parameter influence ranking based on correlation with UTS and mass loss",
    fontsize=13
)

ax.axhline(0, color="black", linewidth=0.9)
ax.legend(loc="upper right", fontsize=11, frameon=True)

fig.tight_layout()

# =========================================================
# Save outputs
# =========================================================
tiff_file = output_dir / "Fig_4_4b_Parameter_Ranking.tiff"
png_file = output_dir / "Fig_4_4b_Parameter_Ranking.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"Saved TIFF: {tiff_file}")
print(f"Saved PNG: {png_file}")

# =========================================================
# Print values for manuscript
# =========================================================
print("\nCorrelation with UTS:")
print(uts_values.round(3))

print("\nCorrelation with Mass Loss:")
print(wear_values.round(3))