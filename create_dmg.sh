#!/bin/bash
set -e

# Directory setup
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Create a clean virtual environment
echo "Creating virtual environment..."
rm -rf venv_build
python3 -m venv venv_build
source venv_build/bin/activate

# Install required packages
echo "Installing requirements..."
pip install -r requirements.txt
pip install py2app

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Package the application
echo "Building app with py2app..."
python setup.py py2app

# Create a DMG file using hdiutil
echo "Creating DMG..."
DMG_NAME="Red-Light-Green-Light-Installer.dmg"
rm -f "$DMG_NAME"

# Create temp folder for DMG contents
DMG_TMP="$(mktemp -d)"
DMG_APP_DIR="$DMG_TMP/Red Light Green Light.app"

# Copy the .app to the temp folder
cp -R "dist/app.app" "$DMG_APP_DIR"

# Create the DMG
hdiutil create -volname "Red Light Green Light" \
               -srcfolder "$DMG_TMP" \
               -ov -format UDZO \
               "$DMG_NAME"

# Clean up
rm -rf "$DMG_TMP"
echo "Done! Created $DMG_NAME"

# Optional - open finder to show the DMG
open -R "$DMG_NAME"