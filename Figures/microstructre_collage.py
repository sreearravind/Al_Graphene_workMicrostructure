import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import numpy as np

# =========================================================
# Configuration
# =========================================================
folder_path = r"C:\Users\HP\OneDrive\2026\Al Graphene\Figures_AlGr\Microstructures"
folder_path = Path(folder_path)

image_files = [f"{i}.tiff" for i in range(1, 13)]

captions = [
    "S1. Al-500", "S2. Al-550", "S3. Al-600",
    "S4. A2-500", "S5. A2-550", "S6. A2-600",
    "S7. A3-500", "S8. A3-550", "S9. A3-600",
    "S10. A4-500", "S11. A4-550", "S12. A4-600"
]

rows = 3
cols = 4

# Get image dimensions
sample_img = Image.open(folder_path / image_files[0])
img_width, img_height = sample_img.size
aspect_ratio = img_height / img_width

# Calculate figure size - exactly fit the images
fig_width = 12  # inches
fig_height = fig_width * aspect_ratio * (rows / cols)

# Create figure with absolutely no spacing
fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 9

# =========================================================
# Load and display images
# =========================================================
for idx, (img_file, caption) in enumerate(zip(image_files, captions)):
    row = idx // cols
    col = idx % cols

    ax = axes[row, col]
    img_path = folder_path / img_file

    try:
        # Load and display image
        img = Image.open(img_path)
        img_array = np.array(img)

        if len(img_array.shape) == 2:
            ax.imshow(img_array, cmap='gray')
        else:
            ax.imshow(img_array)

        ax.axis('off')

        # Add caption as text overlay on top of image (saves space)
        ax.text(0.5, 0.03, caption, transform=ax.transAxes,
                ha='center', va='bottom', fontsize=9, fontweight='bold',
                fontfamily='Times New Roman',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='none', alpha=0.7))

    except Exception as e:
        ax.text(0.5, 0.5, f"Error", ha='center', va='center')
        ax.axis('off')
        print(f"Error loading {img_file}: {e}")

# =========================================================
# Save with zero padding
# =========================================================
output_png = folder_path / "Supplementary_Figures_Table_Tight.png"
output_tiff = folder_path / "Supplementary_Figures_Table_Tight.tiff"
output_pdf = folder_path / "Supplementary_Figures_Table_Tight.pdf"

fig.savefig(output_png, dpi=300, format='png', bbox_inches='tight', pad_inches=0)
fig.savefig(output_tiff, dpi=600, format='tiff', bbox_inches='tight', pad_inches=0)
fig.savefig(output_pdf, dpi=300, format='pdf', bbox_inches='tight', pad_inches=0)

plt.close()

print("✓ ULTRA-TIGHT FIGURE TABLE CREATED")
print(f"  PNG:  {output_png}")
print(f"  TIFF: {output_tiff}")
print(f"  PDF:  {output_pdf}")
print("  Captions overlayed on images - zero additional space")