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

print("Columns in CSV:")
print(df.columns.tolist())

# =========================================================
# Required columns
# =========================================================
x_col = "GNP (wt.%)"
y_col = "Sintering Temperature (°C)"
z_col = "UTS"

# =========================================================
# Extract data
# =========================================================
x = df[x_col].values
y = df[y_col].values
z = df[z_col].values

# Print raw points
print("\nRaw data used for 3D surface:")
for xi, yi, zi in zip(x, y, z):
    print(f"GNP = {xi}, Temp = {yi}, UTS = {zi}")

# =========================================================
# Create interpolation grid
# =========================================================
x_grid = np.linspace(x.min(), x.max(), 100)
y_grid = np.linspace(y.min(), y.max(), 100)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

# Interpolate surface
Z_grid = griddata((x, y), z, (X_grid, Y_grid), method='cubic')

# Fallback for NaN edge regions
Z_grid_linear = griddata((x, y), z, (X_grid, Y_grid), method='linear')
Z_grid = np.where(np.isnan(Z_grid), Z_grid_linear, Z_grid)

# =========================================================
# Pivot-style table for manuscript checking
# =========================================================
pivot_table = df.pivot_table(
    values=z_col,
    index=y_col,
    columns=x_col,
    aggfunc='mean'
)

print("\nPivot table (UTS values):")
print(pivot_table)

# =========================================================
# Plot settings
# =========================================================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')

# =========================================================
# Surface plot
# =========================================================
surf = ax.plot_surface(
    X_grid, Y_grid, Z_grid,
    cmap="viridis",
    edgecolor="none",
    alpha=0.9
)

# Original data points
ax.scatter(
    x, y, z,
    color="red",
    s=45,
    label="Experimental data"
)

# =========================================================
# Axis labels
# =========================================================
ax.set_xlabel("GNP content (wt.%)", labelpad=12, fontsize=12)
ax.set_ylabel("Sintering temperature (°C)", labelpad=12, fontsize=12)
ax.set_zlabel("UTS (MPa)", labelpad=10, fontsize=12)

ax.set_title(
    "The effect of GNP content and sintering temperature on UTS",
    pad=18,
    fontsize=13
)

# View angle
ax.view_init(elev=28, azim=135)

# Colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.7, pad=0.12)
cbar.set_label("UTS (MPa)", fontsize=11)

# Legend
ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.95))

fig.tight_layout()

# =========================================================
# Save outputs
# =========================================================
tiff_file = output_dir / "Fig_4_4c_3D_Surface_UTS.tiff"
png_file = output_dir / "Fig_4_4c_3D_Surface_UTS.png"

fig.savefig(tiff_file, dpi=600, format="tiff", bbox_inches="tight")
fig.savefig(png_file, dpi=300, format="png", bbox_inches="tight")

plt.show()

print(f"\nSaved TIFF: {tiff_file}")
print(f"Saved PNG: {png_file}")