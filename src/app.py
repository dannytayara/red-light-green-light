#!/usr/bin/env python3

import rumps
import time
import threading
import base64
import io
import os
import json
import keyring
from pathlib import Path
from mss import mss
from PIL import Image
from anthropic import Anthropic

class RedGreenLightApp(rumps.App):
    def __init__(self):
        super(RedGreenLightApp, self).__init__("🔴", quit_button=None)
        
        # App constants
        self.APP_NAME = "red-light-green-light"
        self.API_KEY_SERVICE = "anthropic-api"
        self.API_KEY_ACCOUNT = "red-light-green-light"
        
        # Configuration
        self.api_key = self.load_api_key()
        self.check_interval = 10  # seconds
        self.monitoring = False
        self.current_task = self.load_task()
        
        # Menu setup
        self.menu = [
            rumps.MenuItem("Start Monitoring", callback=self.toggle_monitoring),
            rumps.MenuItem("Set Task", callback=self.set_task),
            None,  # Separator
            rumps.MenuItem("Set API Key", callback=self.set_api_key),
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        
        # Monitoring thread
        self.monitor_thread = None
        
    def load_api_key(self):
        """Load API key from keyring or environment"""
        # First try to get from keyring
        api_key = keyring.get_password(self.API_KEY_SERVICE, self.API_KEY_ACCOUNT)
        
        # Fall back to environment variable
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            
        return api_key
        
    def save_api_key(self, api_key):
        """Save API key to keyring"""
        keyring.set_password(self.API_KEY_SERVICE, self.API_KEY_ACCOUNT, api_key)
    
    def get_config_dir(self):
        """Get or create config directory"""
        config_dir = Path.home() / ".config" / self.APP_NAME
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
        
    def load_task(self):
        """Load saved task from config file"""
        try:
            config_file = self.get_config_dir() / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("current_task", "")
        except Exception as e:
            print(f"Error loading task: {e}")
        return ""
        
    def save_task(self, task):
        """Save task to config file"""
        try:
            config_file = self.get_config_dir() / "config.json"
            
            # Load existing config or create new
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
                
            # Update task
            config["current_task"] = task
            
            # Save config
            with open(config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving task: {e}")
    
    def set_api_key(self, _):
        """Set the Anthropic API key"""
        current_key = self.api_key or ""
        # Show only first few chars if key exists
        display_key = current_key[:5] + "..." if current_key else ""
        
        response = rumps.Window(
            message="Enter your Anthropic API key:",
            title="API Key Setup",
            default_text=display_key,
            ok="Save",
            cancel="Cancel",
            secure=True
        ).run()
        
        if response.clicked and response.text:
            self.api_key = response.text
            self.save_api_key(self.api_key)
            rumps.notification(
                title="API Key Updated",
                subtitle="Your Anthropic API key has been saved",
                message="The key is stored securely in your system keychain"
            )
    
    def set_task(self, _):
        """Set the task that the user intends to work on"""
        response = rumps.Window(
            message="What are you planning to work on?",
            title="Set Your Task",
            default_text=self.current_task,
            ok="Save",
            cancel="Cancel"
        ).run()
        
        if response.clicked:
            self.current_task = response.text
            self.save_task(self.current_task)
            rumps.notification(
                title="Task Updated",
                subtitle="Your focus task has been updated",
                message=f"Now monitoring: {self.current_task}"
            )
    
    def toggle_monitoring(self, sender):
        """Start or stop the monitoring process"""
        if not self.api_key:
            rumps.notification(
                title="API Key Missing",
                subtitle="Claude API Key not found",
                message="Please click 'Set API Key' from the menu"
            )
            self.set_api_key(None)
            return
            
        if not self.current_task:
            rumps.notification(
                title="No Task Set",
                subtitle="Please set a task first",
                message="Click 'Set Task' to define what you're working on"
            )
            return
        
        self.monitoring = not self.monitoring
        
        if self.monitoring:
            sender.title = "Stop Monitoring"
            self.title = "🟢"  # Start with green
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.monitor_activity)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
        else:
            sender.title = "Start Monitoring"
            self.title = "🔴"
            # Thread will terminate on next loop
    
    def capture_screen(self):
        """Capture the screen and return base64 encoded image"""
        with mss() as sct:
            monitor = sct.monitors[0]  # Capture the main monitor
            sct_img = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Resize to reduce file size (adjust as needed)
            width, height = img.size
            new_width = 1280
            new_height = int(height * (new_width / width))
            img = img.resize((new_width, new_height))
            
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return img_str
    
    def analyze_screen(self, image_base64):
        """Send screen capture to Claude for analysis"""
        client = Anthropic(api_key=self.api_key)
        
        try:
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                temperature=0,
                system="You are an AI assistant that determines if a user is on task. Your response should be STRICTLY 'ON_TASK' or 'OFF_TASK' without explanation. If you're not sure, respond with 'ON_TASK'.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": f"I am supposed to be working on: {self.current_task}\n\nHere's a screenshot of my current screen. Am I on task? Respond with ONLY 'ON_TASK' or 'OFF_TASK'."
                            },
                            {
                                "type": "image", 
                                "source": {
                                    "type": "base64", 
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"Error analyzing screen: {e}")
            return "ON_TASK"  # Default to on-task in case of error
    
    def monitor_activity(self):
        """Monitor activity at regular intervals"""
        while self.monitoring:
            try:
                # Capture screen
                img_str = self.capture_screen()
                
                # Analyze with Claude
                result = self.analyze_screen(img_str)
                
                # Update status
                if result == "ON_TASK":
                    self.title = "🟢"
                else:
                    self.title = "🔴"
                    rumps.notification(
                        title="Focus Alert",
                        subtitle="You appear to be off task",
                        message=f"Remember your focus: {self.current_task}"
                    )
            except Exception as e:
                print(f"Error in monitoring thread: {e}")
            
            # Wait for next check
            time.sleep(self.check_interval)
    
    def quit_app(self, _):
        """Quit the application"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            # Give the thread time to terminate
            time.sleep(0.5)
        rumps.quit_application()

if __name__ == "__main__":
    print("Starting red-light-green-light app...")
    try:
        RedGreenLightApp().run()
    except Exception as e:
        print(f"Error starting app: {e}")
        import traceback
        traceback.print_exc()