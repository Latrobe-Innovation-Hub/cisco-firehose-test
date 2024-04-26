# Author -----=============================================================
# name: Andrew J. McDonald
# date: 17/07/2023
# =========================================================================

import threading
import subprocess
import index
import os
from pathlib import Path


def run_index():
    global apiKey
    # Start firehose data ingestion
    index.process_active_users()

def run_webserver():
    # Run the Flask application
    subprocess.call(["python", "web_server.py"])

api_key_file = Path("API_KEY.txt")

try:
    # Check if the API key file exists and is not empty
    if api_key_file.exists() and api_key_file.stat().st_size > 0:
        with api_key_file.open() as f:
            apiKey = f.read().strip()
    else:
        # Get the API key and perform authorization
        index.get_API_Key_and_auth()
except:
    index.get_API_Key_and_auth()

# Create and start the threads
thread1 = threading.Thread(target=run_index)
thread2 = threading.Thread(target=run_webserver)

# Set the daemon flag for both threads
thread1.daemon = True
thread2.daemon = True

# Start the threads
thread1.start()
thread2.start()

try:
    # Keep the main thread alive until a KeyboardInterrupt (Ctrl+C) occurs
    while True:
        pass
except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")

print("Both processes finished execution")
