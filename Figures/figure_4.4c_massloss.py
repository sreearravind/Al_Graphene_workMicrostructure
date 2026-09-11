import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

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

# =========================================================
# Required columns
# =========================================================
x_col = "GNP (wt.%)"
y_col = "Sintering Temperature (°C)"
z_col = "Mass Loss (g)"

# =========================================================
# Extract data
# =========================================================
x = df[x_col].values
y = df[y_col].values
z = df[z_col].values

print("\nRaw data used for Mass Loss surface:")
for xi, yi, zi in zip(x, y, z):
    print(f"GNP = {xi}, Temp = {yi}, Mass Loss = {zi}")

# =========================================================
# Create interpolation grid
# =========================================================
x_grid = np.linspace(x.min(), x.max(), 100)
y_grid = np.linspace(y.min(), y.max(), 100)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

# Interpolation
Z_grid = griddata((x, y), z, (X_grid, Y_grid), method='cubic')

# Handle NaNs
Z_linear = griddata((x, y), z, (X_grid, Y_grid), method='linear')
Z_grid = np.where(np.isnan(Z_grid), Z_linear, Z_grid)

# =========================================================
# Pivot table for validation
# =========================================================
pivot_table = df.pivot_table(
    values=z_col,
    index=y_col,
    columns=x_col,
    aggfunc='mean'
)

print("\nPivot table (Mass Loss values):")
print(pivot_table)

# =========================================================
# Plot
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    X_grid, Y_grid, Z_grid,
    cmap="viridis",
    edgecolor="none",
    alpha=0.9
)

# Scatter points
ax.scatter(
    x, y, z,
    color="black",
    s=45,
    label="Experimental data"
)

# Labels
ax.set_xlabel("GNP content (wt.%)", labelpad=12)
ax.set_ylabel("Sintering temperature (°C)", labelpad=12)
ax.set_zlabel("Mass Loss (g)", labelpad=10)

ax.set_title(
    "Effect of GNP content and sintering temperature on Mass Loss",
    pad=18
)

# View
ax.view_init(elev=28, azim=135)

# Colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.7, pad=0.12)
cbar.set_label("Mass Loss (g)")

# Legend
ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.95))

fig.tight_layout()

# =========================================================
# Save
# =========================================================
tiff_file = output_dir / "Fig_4_4c_3D_Surface_MassLoss.tiff"
png_file = output_dir / "Fig_4_4c_3D_Surface_MassLoss.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"\nSaved TIFF: {tiff_file}")
print(f"Saved PNG: {png_file}")