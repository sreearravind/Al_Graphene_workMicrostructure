import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DEFAULT_CSV = r"C:\Users\HP\OneDrive\2026\Al Graphene\Supplementary_Grain_Size_hardness_tensile_desnity.csv"
DEFAULT_OUT = r"C:\Users\HP\OneDrive\2026\Al Graphene\Figures_AlGr\Publication_Ready"


def save_figure(fig, output_dir: Path, stem: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / f"{stem}.png", dpi=600, bbox_inches="tight")
    fig.savefig(
        output_dir / f"{stem}.tiff",
        dpi=600,
        bbox_inches="tight",
        pil_kwargs={"compression": "tiff_lzw"},
    )
    fig.savefig(output_dir / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def configure_plotting():
    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 12,
            "axes.labelsize": 16,
            "axes.titlesize": 15,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 11,
        }
    )


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.sort_values("Sample").reset_index(drop=True)
    df["SampleLabel"] = [f"S{i}" for i in df["Sample"]]
    return df


def figure5(df, output_dir):
    density_candidates = [c for c in df.columns if "Extruded Density" in c]
    if not density_candidates:
        raise ValueError("Extruded Density column not found")
    density_col = density_candidates[0]

    x = np.arange(len(df))
    hardness = df["Hardness (HRB)"].to_numpy()
    density = df[density_col].to_numpy()

    fig, ax1 = plt.subplots(figsize=(11.8, 7.2))
    line1 = ax1.plot(
        x, hardness, marker="o", markersize=8, linewidth=2.2, label="Hardness (HRB)"
    )
    ax1.set_xlabel("Processing condition")
    ax1.set_ylabel("Rockwell hardness (HRB)", fontweight="bold")
    ax1.set_xticks(x, df["SampleLabel"])
    ax1.set_xlim(-0.45, len(df) - 0.55)
    ax1.grid(axis="y", alpha=0.22)

    for i, (xi, yi) in enumerate(zip(x, hardness)):
        dy = 15 if i == 8 else 12 if i == 10 else 10
        ax1.annotate(
            f"{yi:.2f}", (xi, yi), xytext=(0, dy), textcoords="offset points",
            ha="center", fontsize=11, fontweight="bold"
        )

    ax2 = ax1.twinx()
    line2 = ax2.plot(
        x, density, marker="s", linestyle="--", markersize=7, linewidth=2.0,
        label="Extruded density (g/cm³)"
    )
    ax2.set_ylabel("Extruded density (g/cm³)", fontweight="bold")

    density_offsets = {
        4: (-14, -24), 5: (14, -24), 7: (-20, -28),
        8: (20, -28), 9: (-16, -24), 10: (16, -24),
    }
    for i, (xi, yi) in enumerate(zip(x, density)):
        dx, dy = density_offsets.get(i, (0, -18))
        ax2.annotate(
            f"{yi:.3f}", (xi, yi), xytext=(dx, dy), textcoords="offset points",
            ha="center", fontsize=10
        )

    lines = line1 + line2
    ax1.legend(
        lines, [line.get_label() for line in lines], loc="upper center",
        bbox_to_anchor=(0.5, 1.11), ncol=2, frameon=True
    )
    fig.tight_layout()
    save_figure(fig, output_dir, "Figure_5_Hardness_Extruded_Density_Upgraded")


def figure6(df, output_dir):
    x = np.arange(len(df))
    ys = df["Yield Strength"].to_numpy()
    uts = df["UTS"].to_numpy()
    elong = df["Elongation %"].to_numpy()

    fig, ax1 = plt.subplots(figsize=(12.2, 7.3))
    width = 0.36
    bars1 = ax1.bar(x - width / 2, ys, width, label="Yield strength (MPa)")
    bars2 = ax1.bar(x + width / 2, uts, width, label="Ultimate tensile strength (MPa)")
    ax1.set_xlabel("Processing condition")
    ax1.set_ylabel("Strength (MPa)", fontweight="bold")
    ax1.set_xticks(x, df["SampleLabel"])
    ax1.set_ylim(0, max(uts.max() * 1.12, 145))
    ax1.grid(axis="y", alpha=0.20)

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax1.annotate(
                f"{h:.0f}", (bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 5), textcoords="offset points", ha="center",
                fontsize=10.5, fontweight="bold"
            )

    ax2 = ax1.twinx()
    line = ax2.plot(x, elong, marker="o", linewidth=2.4, markersize=8, label="Elongation (%)")
    ax2.set_ylabel("Elongation (%)", fontweight="bold")
    ax2.set_ylim(0, max(33, elong.max() * 1.10))

    for i, (xi, yi) in enumerate(zip(x, elong)):
        dx = -12 if i in (2, 10) else 0
        dy = 5 if i in (2, 10) else 9
        ax2.annotate(
            f"{yi:.1f}", (xi, yi), xytext=(dx, dy), textcoords="offset points",
            ha="center", fontsize=10.5, fontweight="bold"
        )

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3, frameon=True)
    fig.tight_layout()
    save_figure(fig, output_dir, "Figure_6_YS_UTS_Elongation_Upgraded")


def figure8(df, output_dir):
    x = np.arange(len(df))
    cof = df["COF"].to_numpy()
    mass = df["Mass Loss (g)"].to_numpy()

    fig, ax1 = plt.subplots(figsize=(12.0, 7.2))
    line1 = ax1.plot(x, cof, marker="o", markersize=8, linewidth=2.3, label="Coefficient of friction")
    ax1.set_xlabel("Processing condition")
    ax1.set_ylabel("Coefficient of friction (COF)", fontweight="bold")
    ax1.set_xticks(x, df["SampleLabel"])
    ax1.set_xlim(-0.45, len(df) - 0.55)
    ax1.grid(axis="y", alpha=0.22)

    for xi, yi in zip(x, cof):
        ax1.annotate(
            f"{yi:.3f}", (xi, yi), xytext=(0, 10), textcoords="offset points",
            ha="center", fontsize=10.5, fontweight="bold"
        )

    ax2 = ax1.twinx()
    line2 = ax2.plot(x, mass, marker="s", linestyle="--", markersize=7, linewidth=2.1, label="Mass loss (g)")
    ax2.set_ylabel("Mass loss (g)", fontweight="bold")

    for xi, yi in zip(x, mass):
        ax2.annotate(
            f"{yi:.4f}", (xi, yi), xytext=(0, -18), textcoords="offset points",
            ha="center", fontsize=10
        )

    lines = line1 + line2
    ax1.legend(lines, [line.get_label() for line in lines], loc="upper center", bbox_to_anchor=(0.5, 1.11), ncol=2, frameon=True)
    fig.tight_layout()
    save_figure(fig, output_dir, "Figure_8_COF_Mass_Loss_Upgraded")


def figure9(df, output_dir):
    cof = df["COF"].to_numpy()
    mass = df["Mass Loss (g)"].to_numpy()

    fig, ax = plt.subplots(figsize=(10.8, 7.2))
    ax.scatter(cof, mass, s=85, edgecolors="black", linewidths=0.8)

    fit = np.polyfit(cof, mass, 1)
    xline = np.linspace(cof.min(), cof.max(), 200)
    ax.plot(xline, np.polyval(fit, xline), linestyle="--", linewidth=2.0, label="Linear trend")

    offsets = {
        1: (-18, 8), 2: (8, -18), 3: (-2, 8), 4: (8, 8),
        5: (8, 8), 6: (-12, 8), 7: (8, 8), 8: (8, 8),
        9: (8, 8), 10: (8, -18), 11: (-18, 8), 12: (8, 8),
    }
    for idx, (cx, my) in enumerate(zip(cof, mass), start=1):
        dx, dy = offsets[idx]
        ax.annotate(
            f"S{idx}", (cx, my), xytext=(dx, dy), textcoords="offset points",
            fontsize=11, fontweight="bold"
        )

    min_idx = int(np.argmin(mass))
    ax.annotate(
        f"Minimum mass loss (S{min_idx + 1})", (cof[min_idx], mass[min_idx]),
        xytext=(12, 18), textcoords="offset points", fontsize=10.5
    )
    ax.set_xlabel("Coefficient of friction (COF)", fontweight="bold")
    ax.set_ylabel("Mass loss (g)", fontweight="bold")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper right", frameon=True)
    fig.tight_layout()
    save_figure(fig, output_dir, "Figure_9_COF_vs_Mass_Loss_Upgraded")


def correlation_inputs(df):
    numeric_cols = [
        "GNP (wt.%)", "Sintering Temperature (°C)",
        "Mean_Equivalent_grain_Diameter_um", "Hardness (HRB)",
        "Bulk Density (g/cm³)", "Extruded Density", "Yield Strength", "UTS",
        "Elongation %", "Frictional Force (N)", "COF", "Mass Loss (g)",
    ]
    label_map = {
        "GNP (wt.%)": "GNP", "Sintering Temperature (°C)": "Sinter Temp",
        "Mean_Equivalent_grain_Diameter_um": "Grain Size", "Hardness (HRB)": "Hardness",
        "Bulk Density (g/cm³)": "Bulk Density", "Extruded Density": "Extruded Density",
        "Yield Strength": "YS", "UTS": "UTS", "Elongation %": "Elongation",
        "Frictional Force (N)": "Friction Force", "COF": "COF", "Mass Loss (g)": "Mass Loss",
    }
    return numeric_cols, label_map


def figure10(df, output_dir):
    numeric_cols, label_map = correlation_inputs(df)
    corr = df[numeric_cols].corr(method="pearson")
    labels = [label_map[c] for c in numeric_cols]

    fig, ax = plt.subplots(figsize=(12.4, 10.2))
    image = ax.imshow(corr.to_numpy(), vmin=-1, vmax=1, aspect="equal")
    ax.set_xticks(np.arange(len(labels)), labels, rotation=50, ha="right")
    ax.set_yticks(np.arange(len(labels)), labels)

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=10.5, fontweight="bold")

    cbar = fig.colorbar(image, ax=ax, fraction=0.045, pad=0.03)
    cbar.set_label("Pearson correlation coefficient, r", fontsize=14, fontweight="bold")
    cbar.ax.tick_params(labelsize=11)
    fig.tight_layout()
    save_figure(fig, output_dir, "Figure_10_Pearson_Correlation_Matrix_Upgraded")


def figure11(df, output_dir):
    numeric_cols, label_map = correlation_inputs(df)
    corr = df[numeric_cols].corr(method="pearson")

    uts_corr = corr["UTS"].drop("UTS")
    mass_corr = corr["Mass Loss (g)"].drop("Mass Loss (g)")
    common = [p for p in uts_corr.index if p in mass_corr.index]
    ranking = uts_corr[common].abs().sort_values(ascending=False).index
    uts_values = uts_corr[ranking]
    mass_values = mass_corr[ranking]
    labels = [label_map[p] for p in ranking]

    x = np.arange(len(ranking))
    width = 0.36
    fig, ax = plt.subplots(figsize=(12.2, 7.4))
    bars1 = ax.bar(x - width / 2, uts_values, width, label="Correlation with UTS")
    bars2 = ax.bar(x + width / 2, mass_values, width, label="Correlation with mass loss")
    ax.axhline(0, linewidth=1.0)
    ax.set_ylabel("Pearson correlation coefficient, r", fontweight="bold")
    ax.set_xlabel("Parameter", fontweight="bold")
    ax.set_xticks(x, labels, rotation=40, ha="right")
    ax.grid(axis="y", alpha=0.20)

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            offset = 5 if h >= 0 else -16
            ax.annotate(
                f"{h:.2f}", (bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, offset), textcoords="offset points", ha="center",
                fontsize=10.5, fontweight="bold"
            )
    ax.legend(loc="upper right", frameon=True)
    fig.tight_layout()
    save_figure(fig, output_dir, "Figure_11_Correlation_with_UTS_and_Mass_Loss_Upgraded")


def main():
    parser = argparse.ArgumentParser(description="Generate publication-ready Figures 5, 6, 8, 9, 10 and 11 without changing source values.")
    parser.add_argument("--csv", default=DEFAULT_CSV, help="Path to the master CSV used by the original figure scripts")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Output directory")
    args = parser.parse_args()

    configure_plotting()
    df = prepare(pd.read_csv(args.csv, encoding="ISO-8859-1"))
    output_dir = Path(args.out)

    figure5(df, output_dir)
    figure6(df, output_dir)
    figure8(df, output_dir)
    figure9(df, output_dir)
    figure10(df, output_dir)
    figure11(df, output_dir)

    print(f"Publication-ready figures saved to: {output_dir}")


if __name__ == "__main__":
    main()
