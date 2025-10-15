#!/usr/bin/env python3
"""
URL to Android App Converter - Production Setup
Installs dependencies and creates required directories for Render deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    project_root = Path(__file__).parent.resolve()
    
    print("\n" + "="*60)
    print("URL to Android App Converter - Production Setup")
    print("="*60 + "\n")
    
    # Step 1: Install dependencies (no virtual env on Render)
    print("[1/2] Installing dependencies...")
    deps = [
        "beautifulsoup4>=4.14.2", 
        "flask>=3.1.2", 
        "flask-cors>=6.0.1", 
        "pillow>=11.3.0", 
        "requests>=2.32.5",
        "gunicorn>=21.2.0"
    ]
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        
        subprocess.run([
            sys.executable, "-m", "pip", "install"
        ] + deps, check=True, capture_output=True)
        
        print("      ✓ All packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"      ✗ Failed to install dependencies: {e}")
        return False
    
    # Step 2: Create required directories
    print("\n[2/2] Creating directories...")
    for dirname in ['db', 'generated', 'android_templates_apks']:
        dir_path = project_root / dirname
        dir_path.mkdir(exist_ok=True)
        print(f"      ✓ {dirname}/")
    
    # Done
    print("\n" + "="*60)
    print("✓ Setup Complete!")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
