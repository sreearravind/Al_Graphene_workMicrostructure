#!/usr/bin/env python3
"""
Batch BMP to TIFF Converter
Converts all BMP images in specified folders to TIFF format
Supports multiple input paths and preserves folder structure
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
from datetime import datetime
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

# Default settings
DEFAULT_OUTPUT_DIR = "converted_tiff"
DEFAULT_COMPRESSION = "tiff_lzw"  # Options: 'tiff_lzw', 'tiff_deflate', 'tiff_ccitt', None
DEFAULT_DPI = 300
SUPPORTED_FORMATS = ['.bmp', '.BMP']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bmp_to_tiff_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONVERSION FUNCTIONS
# ============================================================================

def convert_bmp_to_tiff(input_path, output_path, compression=None, dpi=None):
    """
    Convert a single BMP image to TIFF format.

    Parameters:
    - input_path: Path to source BMP file
    - output_path: Path for output TIFF file
    - compression: Compression type for TIFF
    - dpi: DPI for the output image

    Returns:
    - Boolean indicating success
    """
    try:
        # Open the BMP image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (BMP might be in different modes)
            if img.mode not in ('RGB', 'L', 'I', 'F'):
                img = img.convert('RGB')

            # Prepare save options
            save_options = {}

            if compression:
                save_options['compression'] = compression

            if dpi:
                save_options['dpi'] = (dpi, dpi)

            # Save as TIFF
            img.save(output_path, 'TIFF', **save_options)

            # Log file size information
            input_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
            output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            compression_ratio = (1 - output_size / input_size) * 100 if input_size > 0 else 0

            logger.info(f"  ✓ Converted: {Path(input_path).name}")
            logger.info(f"    Size: {input_size:.2f} MB → {output_size:.2f} MB ({compression_ratio:.1f}% reduction)")

            return True

    except Exception as e:
        logger.error(f"  ✗ Failed to convert {input_path}: {str(e)}")
        return False


def find_bmp_files(input_paths, recursive=True):
    """
    Find all BMP files in the given paths.

    Parameters:
    - input_paths: List of paths (files or directories)
    - recursive: Search recursively in directories

    Returns:
    - List of Path objects for BMP files
    """
    bmp_files = []

    for path in input_paths:
        path_obj = Path(path)

        if not path_obj.exists():
            logger.warning(f"Path does not exist: {path}")
            continue

        if path_obj.is_file():
            # Single file
            if path_obj.suffix.lower() in SUPPORTED_FORMATS:
                bmp_files.append(path_obj)
            else:
                logger.warning(f"Skipping non-BMP file: {path_obj}")

        elif path_obj.is_dir():
            # Directory - search for BMP files
            if recursive:
                # Recursive search
                for ext in SUPPORTED_FORMATS:
                    bmp_files.extend(path_obj.rglob(f'*{ext}'))
                    bmp_files.extend(path_obj.rglob(f'*{ext.lower()}'))
            else:
                # Only current directory
                for ext in SUPPORTED_FORMATS:
                    bmp_files.extend(path_obj.glob(f'*{ext}'))
                    bmp_files.extend(path_obj.glob(f'*{ext.lower()}'))

    # Remove duplicates and sort
    bmp_files = sorted(list(set(bmp_files)))

    return bmp_files


def get_output_path(input_file, output_base_dir, preserve_structure=True, base_input_dir=None):
    """
    Determine output path for converted TIFF file.

    Parameters:
    - input_file: Path to input BMP file
    - output_base_dir: Base output directory
    - preserve_structure: Whether to preserve folder structure
    - base_input_dir: Base input directory for structure preservation

    Returns:
    - Path object for output file
    """
    if preserve_structure and base_input_dir:
        # Preserve relative path structure
        try:
            rel_path = input_file.relative_to(base_input_dir)
            output_path = Path(output_base_dir) / rel_path.with_suffix('.tiff')
        except ValueError:
            # File is not relative to base input directory
            output_path = Path(output_base_dir) / input_file.with_suffix('.tiff').name
    else:
        # Place all files in a single directory with original names
        output_path = Path(output_base_dir) / f"{input_file.stem}.tiff"

    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    return output_path


def batch_convert(input_paths, output_dir=None, preserve_structure=True,
                  compression=None, dpi=None, recursive=True,
                  overwrite=False, verbose=True):
    """
    Batch convert BMP files to TIFF.

    Parameters:
    - input_paths: List of input paths (files or directories)
    - output_dir: Output directory for converted files
    - preserve_structure: Preserve folder structure
    - compression: Compression type for TIFF
    - dpi: DPI for output images
    - recursive: Search recursively in directories
    - overwrite: Overwrite existing TIFF files
    - verbose: Print detailed progress

    Returns:
    - Dictionary with conversion statistics
    """

    # Set default output directory
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    output_dir_path = Path(output_dir)

    # Find all BMP files
    logger.info("=" * 70)
    logger.info("BATCH BMP TO TIFF CONVERTER")
    logger.info("=" * 70)
    logger.info(f"Input paths: {', '.join(str(p) for p in input_paths)}")
    logger.info(f"Output directory: {output_dir_path.absolute()}")
    logger.info(f"Preserve structure: {preserve_structure}")
    logger.info(f"Recursive search: {recursive}")
    logger.info(f"Compression: {compression or 'None'}")
    logger.info(f"DPI: {dpi or 'Original'}")
    logger.info("-" * 70)

    # Find all BMP files
    bmp_files = find_bmp_files(input_paths, recursive)

    if not bmp_files:
        logger.warning("No BMP files found in the specified paths!")
        return {'total': 0, 'converted': 0, 'failed': 0, 'skipped': 0}

    logger.info(f"Found {len(bmp_files)} BMP file(s) to convert")

    # Determine base input directory for structure preservation
    base_input_dir = None
    if preserve_structure and len(input_paths) == 1 and Path(input_paths[0]).is_dir():
        base_input_dir = Path(input_paths[0])

    # Statistics
    stats = {
        'total': len(bmp_files),
        'converted': 0,
        'failed': 0,
        'skipped': 0,
        'files': []
    }

    # Convert each file
    for i, bmp_file in enumerate(bmp_files, 1):
        if verbose:
            logger.info(f"\n[{i}/{len(bmp_files)}] Processing: {bmp_file}")

        # Determine output path
        output_file = get_output_path(bmp_file, output_dir, preserve_structure, base_input_dir)

        # Check if output already exists
        if output_file.exists() and not overwrite:
            logger.info(f"  ⏭ Skipping (already exists): {output_file}")
            stats['skipped'] += 1
            stats['files'].append({
                'input': str(bmp_file),
                'output': str(output_file),
                'status': 'skipped',
                'reason': 'file_exists'
            })
            continue

        # Convert the file
        success = convert_bmp_to_tiff(bmp_file, output_file, compression, dpi)

        if success:
            stats['converted'] += 1
            stats['files'].append({
                'input': str(bmp_file),
                'output': str(output_file),
                'status': 'converted',
                'size_mb_input': os.path.getsize(bmp_file) / (1024 * 1024),
                'size_mb_output': os.path.getsize(output_file) / (1024 * 1024)
            })
        else:
            stats['failed'] += 1
            stats['files'].append({
                'input': str(bmp_file),
                'output': str(output_file),
                'status': 'failed'
            })

    # Print summary
    logger.info("\n" + "=" * 70)
    logger.info("CONVERSION SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total files found: {stats['total']}")
    logger.info(f"Successfully converted: {stats['converted']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info(f"Skipped (already exist): {stats['skipped']}")
    logger.info(f"Output directory: {output_dir_path.absolute()}")

    # Save statistics to file
    save_statistics(stats, output_dir_path)

    return stats


def save_statistics(stats, output_dir):
    """Save conversion statistics to a CSV file."""
    import csv

    stats_file = output_dir / "conversion_statistics.csv"

    try:
        with open(stats_file, 'w', newline='') as f:
            if stats['files']:
                # Get all keys from the first file
                fieldnames = stats['files'][0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(stats['files'])

        logger.info(f"Statistics saved to: {stats_file}")
    except Exception as e:
        logger.warning(f"Could not save statistics: {e}")


# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def interactive_mode():
    """Run the converter in interactive mode with user prompts."""

    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "   BMP TO TIFF BATCH CONVERTER - INTERACTIVE MODE".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    # Get input paths
    print("\n📁 Enter input paths (files or folders, one per line)")
    print("   Type 'done' when finished:")

    input_paths = []
    while True:
        path = input("   Path: ").strip()
        if path.lower() == 'done':
            break
        if path:
            input_paths.append(path)

    if not input_paths:
        print("❌ No input paths provided. Exiting.")
        return

    # Get output directory
    output_dir = input(f"\n📂 Output directory (default: {DEFAULT_OUTPUT_DIR}): ").strip()
    if not output_dir:
        output_dir = DEFAULT_OUTPUT_DIR

    # Preserve structure?
    preserve = input("\n📁 Preserve folder structure? (y/n, default: y): ").strip().lower()
    preserve_structure = preserve != 'n'

    # Compression
    print("\n🗜 Compression options:")
    print("   1. LZW (default) - Good compression, lossless")
    print("   2. Deflate - Similar to LZW")
    print("   3. None - No compression, largest files")
    print("   4. CCITT - For binary images only")

    compression_choice = input("   Choose (1-4, default: 1): ").strip()
    compression_map = {
        '1': 'tiff_lzw',
        '2': 'tiff_deflate',
        '3': None,
        '4': 'tiff_ccitt'
    }
    compression = compression_map.get(compression_choice, 'tiff_lzw')

    # DPI
    dpi_input = input(f"\n📐 Output DPI (default: {DEFAULT_DPI}, press Enter for default): ").strip()
    dpi = int(dpi_input) if dpi_input else DEFAULT_DPI

    # Overwrite existing
    overwrite = input("\n⚠ Overwrite existing TIFF files? (y/n, default: n): ").strip().lower() == 'y'

    # Verbose
    verbose = input("\n📊 Show detailed progress? (y/n, default: y): ").strip().lower() != 'n'

    # Confirm and convert
    print("\n" + "=" * 70)
    print("📋 CONFIGURATION SUMMARY:")
    print(f"   Input paths: {', '.join(input_paths)}")
    print(f"   Output directory: {output_dir}")
    print(f"   Preserve structure: {preserve_structure}")
    print(f"   Compression: {compression or 'None'}")
    print(f"   DPI: {dpi}")
    print(f"   Overwrite: {overwrite}")
    print("=" * 70)

    confirm = input("\n✅ Start conversion? (y/n): ").strip().lower()

    if confirm == 'y':
        batch_convert(
            input_paths=input_paths,
            output_dir=output_dir,
            preserve_structure=preserve_structure,
            compression=compression,
            dpi=dpi,
            overwrite=overwrite,
            verbose=verbose
        )
    else:
        print("❌ Conversion cancelled.")


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point with command line argument parsing."""

    parser = argparse.ArgumentParser(
        description='Batch convert BMP images to TIFF format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Convert all BMP files in a directory
  python bmp_to_tiff_converter.py ./images -o ./tiff_output

  # Convert multiple directories and preserve structure
  python bmp_to_tiff_converter.py ./100X ./200X ./400X -o ./converted --preserve-structure

  # Convert specific files
  python bmp_to_tiff_converter.py image1.bmp image2.bmp image3.bmp -o ./output

  # Convert with LZW compression and custom DPI
  python bmp_to_tiff_converter.py ./images -o ./output --compression tiff_lzw --dpi 600

  # Interactive mode (no arguments)
  python bmp_to_tiff_converter.py --interactive
        """
    )

    parser.add_argument(
        'input_paths',
        nargs='*',
        help='Input paths (files or directories)'
    )

    parser.add_argument(
        '-o', '--output',
        default=DEFAULT_OUTPUT_DIR,
        help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})'
    )

    parser.add_argument(
        '-p', '--preserve-structure',
        action='store_true',
        help='Preserve folder structure in output'
    )

    parser.add_argument(
        '-c', '--compression',
        choices=['tiff_lzw', 'tiff_deflate', 'tiff_ccitt', 'none'],
        default='tiff_lzw',
        help='Compression type for TIFF (default: tiff_lzw)'
    )

    parser.add_argument(
        '-d', '--dpi',
        type=int,
        default=DEFAULT_DPI,
        help=f'Output DPI (default: {DEFAULT_DPI})'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        default=True,
        help='Search recursively in directories (default: True)'
    )

    parser.add_argument(
        '-w', '--overwrite',
        action='store_true',
        help='Overwrite existing TIFF files'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress detailed output'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    args = parser.parse_args()

    # Handle interactive mode
    if args.interactive or not args.input_paths:
        interactive_mode()
        return

    # Convert compression argument
    compression = None if args.compression == 'none' else args.compression

    # Run batch conversion
    batch_convert(
        input_paths=args.input_paths,
        output_dir=args.output,
        preserve_structure=args.preserve_structure,
        compression=compression,
        dpi=args.dpi,
        recursive=args.recursive,
        overwrite=args.overwrite,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()