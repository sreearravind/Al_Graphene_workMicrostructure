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
# Column names
# =========================================================
sample_col = "Sample"
cof_col = "COF"
mass_col = "Mass Loss (g)"

# =========================================================
# Prepare data
# =========================================================
df = df.sort_values(by=sample_col).reset_index(drop=True)
df["SampleLabel"] = [f"S{i}" for i in df[sample_col]]

sample_meta = {
    "S1":  "Pure Al/500 °C",
    "S2":  "Pure Al/550 °C",
    "S3":  "Pure Al/600 °C",
    "S4":  "Al-2% Gr/500 °C",
    "S5":  "Al-2% Gr/550 °C",
    "S6":  "Al-2% Gr/600 °C",
    "S7":  "Al-3% Gr/500 °C",
    "S8":  "Al-3% Gr/550 °C",
    "S9":  "Al-3% Gr/600 °C",
    "S10": "Al-4% Gr/500 °C",
    "S11": "Al-4% Gr/550 °C",
    "S12": "Al-4% Gr/600 °C",
}
df["MetaLabel"] = df["SampleLabel"].map(sample_meta)

optimal_sample = "S5"
crowded_samples = {"S1", "S2", "S3", "S11"}

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12

fig, ax = plt.subplots(figsize=(13, 8))

# =========================================================
# Scatter + annotations
# =========================================================
for _, row in df.iterrows():
    x = row[cof_col]
    y = row[mass_col]
    sample = row["SampleLabel"]
    meta = row["MetaLabel"]

    # region-based offset logic
    if x > 0.5 and y < 0.006:
        dx_sample, dy_sample = -18, 12
        dx_meta, dy_meta = -18, -18
    elif x < 0.4 and y > 0.006:
        dx_sample, dy_sample = 14, -10
        dx_meta, dy_meta = 14, -26
    else:
        dx_sample, dy_sample = 0, 12
        dx_meta, dy_meta = 0, -15

    # optimal sample
    if sample == optimal_sample:
        ax.scatter(
            x, y,
            s=180,
            color="gold",
            edgecolor="black",
            linewidth=1.2,
            zorder=5
        )

        ax.annotate(
            sample,
            (x, y),
            textcoords="offset points",
            xytext=(dx_sample, dy_sample),
            ha="center",
            fontsize=10,
            fontweight="bold",
            color="black"
        )

        ax.annotate(
            f"({meta})",
            (x, y),
            textcoords="offset points",
            xytext=(dx_meta, dy_meta),
            ha="center",
            fontsize=8.5,
            color="black"
        )

        ax.annotate(
            "Optimal sample",
            (x, y),
            textcoords="offset points",
            xytext=(dx_meta, dy_meta - 14),
            ha="center",
            fontsize=8.5,
            color="darkred",
            fontweight="bold"
        )

    else:
        ax.scatter(
            x, y,
            s=90,
            color="darkblue",
            edgecolor="black",
            linewidth=0.8,
            zorder=3
        )

        # For crowded samples: only short label near point
        if sample in crowded_samples:
            ax.annotate(
                sample,
                (x, y),
                textcoords="offset points",
                xytext=(dx_sample, dy_sample),
                ha="center",
                fontsize=9,
                color="black",
                fontweight="bold"
            )
        else:
            # Other samples: full annotation
            ax.annotate(
                sample,
                (x, y),
                textcoords="offset points",
                xytext=(dx_sample, dy_sample),
                ha="center",
                fontsize=9,
                color="black"
            )

            ax.annotate(
                f"({meta})",
                (x, y),
                textcoords="offset points",
                xytext=(dx_meta, dy_meta),
                ha="center",
                fontsize=8,
                color="black"
            )

# =========================================================
# Linear trendline
# =========================================================
x_vals = df[cof_col].to_numpy()
y_vals = df[mass_col].to_numpy()

z = np.polyfit(x_vals, y_vals, 1)
p = np.poly1d(z)

x_line = np.linspace(min(x_vals), max(x_vals), 200)
y_line = p(x_line)

ax.plot(
    x_line,
    y_line,
    linestyle="--",
    linewidth=1.8,
    color="darkred",
    label="Linear trend"
)

# =========================================================
# Text box for crowded samples
# =========================================================
crowded_note = (
    "Selected sample identifiers:\n"
    "S1  = Pure Al/500 °C\n"
    "S2  = Pure Al/550 °C\n"
    "S3  = Pure Al/600 °C\n"
    "S11 = Al-4% Gr/550 °C"
)

ax.text(
    0.03, 0.97,
    crowded_note,
    transform=ax.transAxes,
    fontsize=9,
    va="top",
    ha="left",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="black", alpha=0.9)
)

# =========================================================
# Axis labels and title
# =========================================================
ax.set_xlabel("Coefficient of Friction (COF)", fontsize=13)
ax.set_ylabel("Mass Loss (g)", fontsize=13)
plt.title("Relationship between coefficient of friction and mass loss", fontsize=14)

# =========================================================
# Legend (trend only)
# =========================================================
ax.legend(
    loc="upper right",
    frameon=True,
    fontsize=11
)

# =========================================================
# Layout and save
# =========================================================
fig.tight_layout()

tiff_file = output_dir / "Fig_4_3b_COF_vs_MassLoss_Final.tiff"
png_file = output_dir / "Fig_4_3b_COF_vs_MassLoss_Final.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"TIFF saved to: {tiff_file}")
print(f"PNG saved to:  {png_file}")