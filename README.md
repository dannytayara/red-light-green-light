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
- Python 3.7+
- Anthropic API key (for Claude)

## Installation

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
4. Your Anthropic API key will be requested when you start the app for the first time
   (The key will be stored securely in your system keychain)

## Usage

1. Run the app:
   ```
   python src/app.py
   ```
2. Click on the menu bar icon (initially 🔴)
3. Select "Set Task" and enter what you're working on
4. Select "Start Monitoring" to begin tracking
5. The menu bar icon will change to 🟢 when you're on task and 🔴 when you're off task