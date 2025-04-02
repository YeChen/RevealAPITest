#this script is created to help MT3 find a way to retrieve COSMIC scrores using API

import requests
import os
import json

# Step 1: setup, retrieve USER and PASSWORD secrets from Colab or os 
username = 'nexlp'
password = os.getenv('DEMO_PASSWORD')
baseurl = "https://consulting.us-east-1.reveal11.cloud"
case_id = 1982
cosmic_id = 3 
start_round = 2 
end_round = 10 


if not username or not password:
    raise ValueError("Secrets USER and PASSWORD must be set in Colab.")

# Step 1: login
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

# Step 2: retrieve doc counts for each round
def get_scores(login_session_id, user_id, case_id, cosmic_id, start_round, end_round):
    """
    Retrieves a list of projects for the authenticated user and prints each project name.
    """
    score_url = baseurl + "/rest/api/v2/revealai/caseid/" + str(case_id) + "/cosmicreports/getscoredistributionreport/" + str(cosmic_id) + "/displayIncrementBeginning/" + str(start_round) + "/displayIncrementEnd/" + str(end_round)

    # Set headers for the GET request, including the incontrolauthtoken
    headers = {
        "Authorization": f"Bearer {login_session_id}",
        "incontrolauthtoken": login_session_id,
        "User-Agent": "Reveal-API-Tester/1.0",
        "Accept": "application/json"
    }

    # Parameters for GET request
    params = {"userId": user_id}

    # Send GET request to retrieve projects
    response = requests.get(score_url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response to get project list
    score_data = response.json()

    # Print each project name
    if score_data:       
        for record in score_data["value"]:
            print("Round ID:" + str(record["roundId"]) + " Score:" + str(record["score"]) + " Score Count:" + str(record["scoreCount"]))             
    else:
            print("No score found.")

# Main Execution
try:
    # Step 1: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 2: Retrieve new project name to use
    project_to_create = get_scores(session_id, user_id, case_id, cosmic_id, start_round, end_round)

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")