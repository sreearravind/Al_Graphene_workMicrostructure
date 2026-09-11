import subprocess
import sys

packages = [
    'numpy',
    'scipy',
    'scikit-image',
    'matplotlib',
    'pandas',
    'pillow',
    'seaborn'
]


def check_and_install():
    missing = []
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing.append(package)

    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("\nAll packages installed successfully!")
    else:
        print("\nAll packages are already installed!")


if __name__ == "__main__":
    check_and_install()