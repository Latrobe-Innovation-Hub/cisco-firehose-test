# Author -----=============================================================
# name: Andrew J. McDonald
# date: 17/07/2023
# =========================================================================

import jwt
import requests
from requests.exceptions import RequestException, ChunkedEncodingError
from urllib3.exceptions import InvalidChunkLength
import json
import socket
import time
import os
import sys
import datetime
from pathlib import Path

def print_nested_keys_values(dictionary, indent=''):
    """
    Recursively prints the keys and values of a nested dictionary.

    Parameters:
        dictionary (dict): The dictionary to print.
        indent (str): The indentation string for nested levels.

    Returns:
        None
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            # If the value is a nested dictionary, print the key and recursively call the function
            print(f"{indent}{key}:")
            print_nested_keys_values(value, indent + '  ')
        else:
            # If the value is not a dictionary, print the key and its corresponding value
            print(f"{indent}{key}: {value}")


def get_API_Key_and_auth():
    """
    Retrieves the API key and performs authorization for the app.

    Returns:
        str: The API key obtained from the authorization process.
    """

    # Get the public key from the specified URL
    print("-- No API Key Found --")
    pubKey = requests.get('https://partners.dnaspaces.io/client/v1/partner/partnerPublicKey/')
    print(pubKey)

    # Parse the public key from the response
    pubKey = json.loads(pubKey.text)
    pubKey = pubKey['data'][0]['publicKey']
    pubKey = '-----BEGIN PUBLIC KEY-----\n' + pubKey + '\n-----END PUBLIC KEY-----'
    print('======= pubKey =======\n', pubKey, '\n')

    # Prompt the user to enter the generated token
    token = input('Enter token here: ')

    # Decode the JSON Web Token using the public key
    decodedJWT = jwt.decode(token, pubKey, algorithms=['RS256'])
    decodedJWT = json.dumps(decodedJWT, indent=2)
    print('======= decodedJWT =======\n', decodedJWT, '\n')

    # Extract required values from the decoded JWT
    decodedJWTJSON = json.loads(decodedJWT)
    appId = decodedJWTJSON['appId']
    activationRefId = decodedJWTJSON['activationRefId']

    # Create payloads and headers for app activation
    authKey = 'Bearer ' + token
    payload = {'appId': appId, 'activationRefId': activationRefId}
    header = {'Content-Type': 'application/json', 'Authorization': authKey}

    # Send a request to activate the app
    activation = requests.post('https://partners.dnaspaces.io/client/v1/partner/activateOnPremiseApp/', headers=header, json=payload)
    activation = json.loads(activation.text)
    print('======= activation[message] =======\n', activation['message'], '\n')

    apiKey = activation['data']['apiKey']
    
    # Write the API key to a file
    with open("API_KEY.txt", "a") as f:
        f.write(apiKey)

    return apiKey

def process_active_users():
    try:
        # init list for actice user data
        activeUsers = []

        # Workaround to get IP address on hosts with non-resolvable hostnames
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP_ADDRESS = s.getsockname()[0]
        s.close()

        # Construct the base URL
        url = 'http://' + str(IP_ADDRESS) + '/'
        
        # set api key file location
        api_key_file = Path("API_KEY.txt")

        try:
            # Check if the API key file exists and is not empty
            if api_key_file.exists() and api_key_file.stat().st_size > 0:
                with api_key_file.open() as f:
                    apiKey = f.read().strip()
                
                print("-- API Key Found --")
                print("-- If you want to renew your API key, just delete the file API_KEY.txt --")
            else:
                # Get the API key and perform authorization
                apiKey = get_API_Key_and_auth()
        except:
            # Get the API key and perform authorization if an exception occurs
            apiKey = get_API_Key_and_auth()

        # Create a session with the API key as the header
        s = requests.Session()
        s.headers = {'X-API-Key': apiKey}

        
        try:
            # Make a streaming request to the API
            response = s.get('https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)

            # Check the response status code
            if response.status_code != 200:
                print("Error: Request failed with status code", response.status_code)
            else:
                try:
                    # Process each line of the response
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            event = json.loads(decoded_line)
                            eventType = event['eventType']

                            if eventType == "USER_PRESENCE":
                                try:
                                    # Extract relevant data from the event
                                    locationActiveUsers = event['userPresence']['activeUsersCount']['totalUsers']
                                    locationID = event['userPresence']['location']['locationId']
                                    locationName = event['userPresence']['location']['name']
                                    locationType = event['userPresence']['location']['inferredLocationTypes']
                                    locationParentName = event['userPresence']['location']['parent']['name']
                                    locationParentParentName = event['userPresence']['location']['parent']['parent']['name']

                                    # Create a dictionary for the active user data
                                    active_user_data = {
                                        'locationName': locationName,
                                        'activeUsers': locationActiveUsers,
                                        'locationID': locationID,
                                        'locationType': locationType,
                                        'locationParentName': locationParentName,
                                        'locationParentParentName': locationParentParentName,
                                        'lastUpdateTime': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                    }

                                    # Check if the location already exists in the activeUsers list
                                    existing_location_index = next((index for index, user in enumerate(activeUsers) if user['locationID'] == locationName), None)

                                    if existing_location_index is None:
                                        # Add the location to the activeUsers list
                                        activeUsers.append(active_user_data)
                                        print("Location added:", active_user_data['locationID'], active_user_data['activeUsers'])
                                    else:
                                        # Update the existing location in the activeUsers list
                                        activeUsers[existing_location_index] = active_user_data
                                        print("Location updated:", active_user_data['locationID'], active_user_data['activeUsers'])
                                except:
                                    pass

                        print("Total locations on record:", len(activeUsers))
                        
                        # Calculate the total active users for all locations - maybe display on html?
                        #total_active_users = sum(location['activeUsers'] for location in activeUsers)
                        #print("Total Active Users:", total_active_users)

                        # Send the activeUsers data as a payload to the URL
                        payload = {'activeUsers': activeUsers}

                        # prevent race condition with webserver
                        try:
                            r = requests.post(url, json=payload)
                            #print(r.text)
                        except:
                            pass
                        
                except (ChunkedEncodingError, InvalidChunkLength) as e:
                    print("Error occurred while reading response:", e)
                    
        except RequestException as e:
            print("An error occurred during the request:", e)
            
    # catcht ctlr-c and exit gracefully
    except KeyboardInterrupt:
        print("Process interrupted. Exiting...")
        
if __name__ == "__main__":
    process_active_users()
