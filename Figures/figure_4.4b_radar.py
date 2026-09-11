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
# Independent process / structure parameters only
# =========================================================
params = [
    "GNP (wt.%)",
    "Sintering Temperature (°C)",
    "Mean_Equivalent_grain_Diameter_um",
    "Hardness (HRB)",
    "Bulk Density (g/cm³)",
    "Extruded Density"
]

label_map = {
    "GNP (wt.%)": "GNP",
    "Sintering Temperature (°C)": "Sinter Temp",
    "Mean_Equivalent_grain_Diameter_um": "Grain Size",
    "Hardness (HRB)": "Hardness",
    "Bulk Density (g/cm³)": "Bulk Density",
    "Extruded Density": "Extruded Density"
}

target_uts = "UTS"
target_wear = "Mass Loss (g)"

# =========================================================
# Pearson correlations
# =========================================================
corr = df[params + [target_uts, target_wear]].corr(method="pearson")

uts_corr = corr[target_uts].loc[params]
wear_corr = corr[target_wear].loc[params]

# Use absolute values for ranking radar magnitude
# Normalize to [0,1] for better radar visibility
uts_raw = uts_corr.abs().values
wear_raw = wear_corr.abs().values
uts_values = uts_raw / np.max(uts_raw)
wear_values = wear_raw / np.max(wear_raw)
labels = [label_map[p] for p in params]

# =========================================================
# Radar chart helper
# =========================================================
def make_radar(ax, values, labels, color, title):
    N = len(labels)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_closed = values.tolist() + [values[0]]
    angles_closed = angles + [angles[0]]

    ax.plot(angles_closed, values_closed, color=color, linewidth=2.8)
    ax.fill(angles_closed, values_closed, color=color, alpha=0.25)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10)

    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.5", "0.75", "1.0"], fontsize=9)
    ax.set_ylim(0, 1.1)

    # Title slightly above to avoid overlap
    ax.set_title(title, y=1.14, fontsize=13, fontweight="bold")

    # Annotate values slightly outward from data points
    for angle, value in zip(angles, values):
        ax.text(
            angle,
            min(value + 0.08, 1.03),
            f"{value:.2f}",
            ha="center",
            va="center",
            fontsize=9,
            color=color,
            fontweight="bold"
        )

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

fig, axes = plt.subplots(
    1, 2,
    figsize=(13.5, 6.8),
    subplot_kw=dict(polar=True)
)

make_radar(
    axes[0],
    uts_values,
    labels,
    color="blue",
    title="UTS Influence Ranking"
)

make_radar(
    axes[1],
    wear_values,
    labels,
    color="green",
    title="Mass Loss Influence Ranking"
)

plt.suptitle(
    "Fig. 4.4b. Radar-based parameter influence ranking from Pearson correlation analysis",
    fontsize=14,
    y=1.03
)

fig.tight_layout()

# =========================================================
# Save outputs
# =========================================================
tiff_file = output_dir / "Fig_4_4b_Radar_Parameter_Ranking.tiff"
png_file = output_dir / "Fig_4_4b_Radar_Parameter_Ranking.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"Saved TIFF: {tiff_file}")
print(f"Saved PNG: {png_file}")

# =========================================================
# Print numerical values for manuscript
# =========================================================
print("\nAbsolute Pearson correlation magnitude with UTS:")
for label, val in zip(labels, uts_values):
    print(f"{label}: {val:.3f}")

print("\nAbsolute Pearson correlation magnitude with Mass Loss:")
for label, val in zip(labels, wear_values):
    print(f"{label}: {val:.3f}")