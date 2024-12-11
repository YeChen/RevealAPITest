# This test script is used to test Ask functions

import requests
import os

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

# Step 2: create classifier
def run_create_classifier(login_session_id, tag_name):
   
    #1844 is case "API_Standard" in consulting
    tag_url = baseurl + "/rest/api/v2/1844/tags"

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
    #type: 1: multi-select; 2: mutual exclusive
    #prediction: for multi-selection, 1 meeans AI enabled, 0 means Not AI enabled; for mutual exclusive, 1 means Yes, -1 means No 
    payload = {
        "name": tag_name,
        "description": "responsive",
        "type": 2, 
        "recursive": 0,
        "updatable": 1,
        "choices": [
            {
            "name": "Yes",
            "description": "yes",
            "isPrivileged": 1,
            "prediction": 1  
            },
            {
            "name": "No",
            "description": "no",
            "isPrivileged": 1,
            "prediction": -1  
            }
        ]
    }

    # Send POST to create classifier
    response = requests.post(tag_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response
    create_response = response.json()
    tag_id = create_response.get("id", {})

    if tag_id is not None:
        print(f"tag id: {tag_id}")
    else:
        print("Total Results not found in the response.")

    return tag_id

# Step 3: add and run model
def run_model_classifier(login_session_id, tagid):
   
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

    #get model id based on tagid 
    get_model_url = baseurl + "/rest/api/v2/1844/tags/" + tagid
    response = requests.get(get_model_url, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails
    get_model_response = response.json()
    modelid = next((choice.get("aiModelId") for choice in get_model_response.get("choices", []) if "aiModelId" in choice), None)

    #1844 is case "API_Standard" in consulting
    add_model_url = baseurl + "/rest/api/v2/revealai/caseid/1844/referencedmodels"

    # Payload data
    # modelLibraryId: 5 is bullying & toxic behavior
    payload ={"modelId": str(modelid),"modelLibraryId":5}

    # Send POST to add model
    response = requests.post(add_model_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails
    
    #run model
    run_model_url = baseurl + "/rest/api/v2/revealai/caseid/1844/cosmic/" + str(modelid)  + "/run"
    response = requests.post(run_model_url, json="{}", headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

# Main Execution
try:
    # Step 1: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 2: create classifier 
    # tag name needs to be updated each time we run this testing
    tagid = run_create_classifier(session_id, "T02")

    # Step 3: add model and kick off  
    run_model_classifier(session_id, str(tagid))

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")