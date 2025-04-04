# This test script is used to test search CRUD functions

import requests
import os

# Step 1: setup, retrieve USER and PASSWORD secrets from Colab or os 
#username = userdata.get("DEMO_USER")
#password = userdata.get("DEMO_PASSWORD")
username = 'nexlp'
password = os.getenv('DEMO_PASSWORD')
baseurl = "https://consulting.us-east-1.reveal11.cloud"

if not username or not password:
    raise ValueError("Secrets USER and PASSWORD must be set in Colab.")

# Step 2: Define the authentication function
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

# Step 3: Define the function to retrieve projects
def run_search(login_session_id):
   
    #1374 is case "Enron Summit 2024" in consulting
    search_url = baseurl + "/rest/api/v2/1374/search"

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
    payload = {"dateHistogramCriteria":[{"timeInterval":"Auto","fieldName":"CREATION_DATE","start":0,"count":100}],"documentCriteria":{"getFields":'false',"getMandatoryFields":'false',"getSpecialIconFields":'false',"count":0},"queryString":"{\"exact\":true,\"fieldName\":\"FILE_EXTENSION\",\"value\":\"doc\",\"type\":\"metadata\"}","queryType":"Bql"}

    # Send GET request to retrieve projects
    response = requests.post(search_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response to get project list
    search_response = response.json()
    total_results = search_response.get("documentResults", {}).get("totalResults")

    if total_results is not None:
        print(f"Total Results: {total_results}")
    else:
        print("Total Results not found in the response.")
    
# Main Execution
try:
    # Step 2: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 3: run search against Enron Summit
    run_search(session_id)

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")