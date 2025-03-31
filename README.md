# red-light-green-light

A simple macOS menu bar app that helps you stay focused by monitoring your screen and providing visual feedback based on whether you're on task.

## Features

- 🔴 / 🟢 Menu bar indicator showing your current focus status
- Screen capture every 30 seconds for task monitoring
- Claude AI-powered analysis to determine if you're on task
- Simple interface to set your current task
- Desktop notifications when you go off task

## Requirements

- macOS
- Anthropic API key (for Claude)

## Installation

### Easy Install (Recommended)

1. Download the latest DMG installer from the [Releases](https://github.com/dannytayara/red-light-green-light/releases) page
2. Open the DMG file
3. Drag "Red Light Green Light.app" to your Applications folder
4. Open from Applications
5. Your Anthropic API key will be requested when you start the app for the first time
   (The key will be stored securely in your system keychain)

### Run from Source

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies in the virtual environment:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python src/app.py
   ```
5. Your Anthropic API key will be requested when you start the app for the first time
   (The key will be stored securely in your system keychain)

### Building the App

To build the app as a standalone .app bundle and create a DMG installer:

1. Make sure you have the repository cloned
2. Run the build script:
   ```
   ./create_dmg.sh
   ```
3. The script will create a DMG installer in the root directory

## Usage

1. Launch the app from your Applications folder
2. Click on the menu bar icon (initially 🔴)
3. Select "Set Task" and enter what you're working on
4. Select "Start Monitoring" to begin tracking
5. The menu bar icon will change to 🟢 when you're on task and 🔴 when you're off task