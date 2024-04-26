# Author -----=============================================================
# name: Andrew J. McDonald
# date: 17/07/2023
# =========================================================================

from flask import Flask, render_template, request, jsonify
import json
import datetime

app = Flask(__name__)

activeUsers = []
total_active_users = 0

def Update(data):
    # Update the activeUsers list based on the received data
    decoded_data = data.decode("utf-8")
    json_data = json.loads(decoded_data)
    activeUsers = json_data['activeUsers']
    
    # Calculate the total active users for all locations
    total_active_users = sum(location['activeUsers'] for location in activeUsers)

    return activeUsers, total_active_users

@app.route('/', methods=['GET', 'POST'])
def main_page():
    global activeUsers, total_active_users

    if request.method == 'POST':
        try:
            # Get the data from the request
            data = request.data
            
            # Update the activeUsers list using the received data
            activeUsers, total_active_users = Update(data)
            
            # Return a success message with the received data
            return 'Successful update with: ' + str(data)
        
        except ValueError:
            # Return an error message if the data format is invalid
            return 'Invalid data format'

    # Print activeUsers and its type for debugging
    #print(activeUsers)
    #print(type(list(activeUsers)))
    #print(total_active_users)
    
    # Get the current datetime
    current_datetime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Render the 'index.html' template with activeUsers and datetime as variables
    return render_template('index.html',
                            activeUsers=activeUsers,
                            total_active_users=total_active_users,
                            datetime=current_datetime)
    
@app.route('/get_active_users', methods=['GET'])
def get_active_users():
    # Return the activeUsers list as a JSON response
    return jsonify(activeUsers)

if __name__ == "__main__":
    # Start the Flask application
    app.run(host="0.0.0.0", port=80, debug=True)
