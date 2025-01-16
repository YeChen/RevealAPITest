# This test script is used to test Ask functions

import requests
import os
import json

#setup, retrieve USER and PASSWORD secrets from Colab or os 
#username = userdata.get("DEMO_USER")
#password = userdata.get("DEMO_PASSWORD")
username = 'nexlp'
password = os.getenv('DEMO_PASSWORD')
baseurl = "https://consulting.us-east-1.reveal11.cloud"

if not username or not password:
    raise ValueError("Secrets USER and PASSWORD must be set in Colab.")

# Step 1: Define the authentication function
def authenticate(username, password):
    """
    Authenticates with the Reveal API using username and password.
    Returns loginSessionId and userId if authentication is successful.
    """
    login_url = baseurl + "/rest/api/v2/login"
    login_data = {
        "username": username,
        "password": password
    }

    # Define headers for the POST request
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Reveal-API-Tester/1.0"
    }

    # Send POST request to login
    response = requests.post(login_url, json=login_data, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response to get loginSessionId and userId
    login_response = response.json()
    login_session_id = login_response.get("loginSessionId")
    user_id = login_response.get("userId")

    if not login_session_id or not user_id:
        raise ValueError("Failed to retrieve loginSessionId and userId from login response.")

    print("Authentication successful!")
    return login_session_id, user_id

# Step 2: read score
def run_read_score(login_session_id):
   
    #1844 is case "API_Standard" in consulting
    search_url = baseurl + "/rest/api/v2/1844/search"

    # Headers
    headers = {    
      "incontrolauthtoken": login_session_id,
      "Accept": "application/json, text/plain, */*", 
      "accept-encoding": "gzip, deflate, br, zstd",
      "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
      "content-length": "99",
      "Content-Type": "application/json",
      "origin": baseurl,
      "priority": "u=1, i",
      "referer": baseurl + "/admin/companies/1/projects",
      "sec-ch-ua":'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
      "sec-ch-ua-platform":"Windows",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    # Payload data
    # we will just read the first 25 docs back, using Profile 4, and check results
    payload = {
        "documentCriteria":{
            "start":0,
            "count":25,
            "fieldProfileId":4
            }
        }

    # Send POST to create classifier
    response = requests.post(search_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response
    #create_response = response.json()
    #data = json.loads(create_response)
    data = response.json()
    scores = [
        doc["fields"]["_TAGSET_16_SCORE"]
        for doc in data["documentResults"]["documents"]
    ]
    total_score = sum(scores)

    if total_score > 0:    
        print(f"Succeed. The total score is: {total_score}")
    else:
        print("Total Results not found in the response.")

    return "success"

# Main Execution
try:
    # Step 1: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 2: ts16~Hot is a pre-built model
    # case: API_Stantard, ID: 1844
    # fields profile: Hot Document Scores, Field profile ID: 4 
    # read score back, score field: Reveal AI Score - Hot    
    run_read_score(session_id)

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")