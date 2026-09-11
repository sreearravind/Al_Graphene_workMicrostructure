import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

HERE = Path(__file__).resolve().parent
df = pd.read_csv(HERE / "comment10_factor_comparison_data.csv")

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
})

responses = [
    ("Extruded_Density_g_cm3", "Extruded density (g/cm³)", "(a) Extruded density"),
    ("Mean_Equivalent_Grain_Diameter_um", "Mean equivalent grain diameter (µm)", "(b) Grain size"),
    ("Hardness_HRB", "Hardness (HRB)", "(c) Rockwell hardness"),
    ("UTS_MPa", "Ultimate tensile strength (MPa)", "(d) Ultimate tensile strength"),
    ("COF", "Coefficient of friction", "(e) Coefficient of friction"),
    ("Mass_Loss_g", "Mass loss (g)", "(f) Mass loss"),
]

markers = ["o", "s", "^"]
fig, axes = plt.subplots(2, 3, figsize=(12, 7.8), sharex=True)
axes = axes.ravel()

for ax, (col, ylabel, title) in zip(axes, responses):
    for marker, temp in zip(markers, [500, 550, 600]):
        sub = df[df["Sintering_Temperature_C"] == temp].sort_values("GNP_wt_pct")
        ax.plot(
            sub["GNP_wt_pct"], sub[col],
            marker=marker, linewidth=1.8, markersize=5.5,
            label=f"{temp} °C"
        )
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_xticks([0, 2, 3, 4])
    ax.grid(True, alpha=0.22)

for ax in axes[3:]:
    ax.set_xlabel("GNP content (wt.%)")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles, labels,
    loc="upper center", ncol=3,
    frameon=False, bbox_to_anchor=(0.5, 1.01)
)
fig.suptitle(
    "Coupled effects of GNP content and sintering temperature on Al–GNP responses",
    y=1.055, fontsize=12, fontweight="bold"
)
fig.tight_layout(rect=[0, 0, 1, 0.96])

fig.savefig(HERE / "Fig_12_Comparative_Factor_Response.png", dpi=600, bbox_inches="tight")
fig.savefig(
    HERE / "Fig_12_Comparative_Factor_Response.tiff",
    dpi=600, bbox_inches="tight",
    pil_kwargs={"compression": "tiff_lzw"}
)
fig.savefig(HERE / "Fig_12_Comparative_Factor_Response.svg", bbox_inches="tight")
plt.show()
