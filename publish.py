#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to build and publish the package to PyPI.
Usage:
    python publish.py --test    # Upload to TestPyPI
    python publish.py          # Upload to PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Fix Windows encoding issues
if sys.platform.startswith('win'):
    import locale
    # Set environment variables to handle Unicode properly
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")

    # Set environment for better encoding handling
    env = os.environ.copy()
    if sys.platform.startswith('win'):
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env
        )

        if check and result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            sys.exit(1)
        return result

    except UnicodeDecodeError as e:
        print(f"Encoding error running command: {cmd}")
        print(f"Error: {e}")
        if check:
            sys.exit(1)
        return None

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', 'src/*.egg-info']
    for pattern in dirs_to_clean:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed {path}")

def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")

def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("Uploading to TestPyPI...")
    print("Note: You need to configure your TestPyPI API token first.")

    # Try non-interactive first, fall back to interactive
    cmd = "python -m twine upload --repository testpypi --disable-progress-bar --non-interactive dist/*"
    result = run_command(cmd, check=False)

    if result and result.returncode != 0:
        print("Non-interactive upload failed. Trying interactive mode...")
        cmd = "python -m twine upload --repository testpypi --disable-progress-bar dist/*"
        run_command(cmd)

def upload_to_pypi():
    """Upload to PyPI."""
    print("Uploading to PyPI...")
    print("Note: You need to configure your PyPI API token first.")

    # Try non-interactive first, fall back to interactive
    cmd = "python -m twine upload --disable-progress-bar --non-interactive dist/*"
    result = run_command(cmd, check=False)

    if result and result.returncode != 0:
        print("Non-interactive upload failed. Trying interactive mode...")
        cmd = "python -m twine upload --disable-progress-bar dist/*"
        run_command(cmd)

def check_requirements():
    """Check if required tools are installed."""
    required_tools = ['build', 'twine']
    for tool in required_tools:
        result = run_command(f"python -m {tool} --help", check=False)
        if result.returncode != 0:
            print(f"Please install {tool}: pip install {tool}")
            sys.exit(1)

def main():
    """Main function."""
    test_mode = '--test' in sys.argv
    
    print("PyQt Toast Enhanced - Package Publisher")
    print("=" * 40)
    
    # Check requirements
    check_requirements()
    
    # Clean previous builds
    clean_build()
    
    # Build package
    build_package()
    
    # Upload
    if test_mode:
        print("\nUploading to TestPyPI...")
        upload_to_testpypi()
        print("\nPackage uploaded to TestPyPI successfully!")
        print("You can install it with:")
        print("pip install --index-url https://test.pypi.org/simple/ pyqttoast-enhanced")
    else:
        print("\nUploading to PyPI...")
        response = input("Are you sure you want to upload to PyPI? (y/N): ")
        if response.lower() == 'y':
            upload_to_pypi()
            print("\nPackage uploaded to PyPI successfully!")
            print("You can install it with:")
            print("pip install pyqttoast-enhanced")
        else:
            print("Upload cancelled.")

if __name__ == "__main__":
    main()
