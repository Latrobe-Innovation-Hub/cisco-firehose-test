## How to run  
  
1. Clone or download the Git repository to your local machine.  

2. Install the required libraries by running the following command in your terminal or command prompt:  

   ```shell
   pip install -r requirements.txt
   ```

3. In the project's working directory, start the demo by running the following command:  
   ```shell
   python start.py
   ```
   
   Note: If this is your first time running the demo or the api key has expired, you will be prompted to enter a token...  
   
4. To generate an API token, follow these steps:  
   - Go to Cisco DNA Spaces Partner Sandbox at: https://partners.dnaspaces.io/  
   - Click on the gear icon for the 'IH-TEST2' app.  
   - Select 'Renew' and then 'Generate Activation Key'.  
   - Copy the generated key.  
   - Input the key when prompted.
   - working key as of august 2024: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhcHBJZCI6ImFwcC1FQkVBQTQwNzU3Mjg0OUE3ODJGRkFCQzgzMEY3NjFCQyIsInZlcnNpb24iOiJ2MSIsImFjdGl2YXRpb25SZWZJZCI6IjU3RTM3MDVBNzZERTQzOURBREY0QTE4REU1REY0Q0UwIiwiY3VzdG9tZXIiOiJsYXRyb2JlLmVkdS5hdSIsImV4cGlyZXNJbiI6MTcyMzk3MTg1ODI2NCwidGVuYW50SWQiOjE2NzY4LCJiYXNlVXJsIjoiaHR0cHM6Ly9wYXJ0bmVycy5kbmFzcGFjZXMuaW8iLCJwYXJ0bmVyVGVuYW50SWQiOiI4NkIwQTA2QjRFMzI0RDgyQTdBNTY2RjUwMTg5NTkwMSIsImlhdCI6MTcyMzYxNTQ1OCwiZXhwIjoxNzIzOTcxODU4fQ.FTItdRYkS9DVvQ4h6pEgNrDGkzxscXcQLtXLpFzMdqXh2PlTLcxOpQd7VtqGwNX54fOWps1R87HESGuamaRZQyBtoD9yqEt_QEhz__UZewBcdZiCD0wDyNp2bL2EIDqYWsvPIPF4pxXg3nYK7OQXvSs71RxncQDxEC3nuM0N4mc   
   
5. The demo will start sending and receiving active user data through the Cisco Firehose API.  
   - The Cisco Firehose API sends 'event' messages.  
   - This demo listens for 'USER_PRESENCE' events and records the current active users for a given event location.  
   - The active user data is then sent to the web dashboard for viewing.  

6. To view the dashboard, simply visit [http://127.0.0.1/](http://127.0.0.1/) or [http://your-ip/](http://your-ip/) in your web browser.

7. To exit/stop, simply ctlr-c from the terminal.
  
![screenshot](screenshots/screenshot.jpg)

