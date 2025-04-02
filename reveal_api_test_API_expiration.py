# This test script is used to test Document Text CRUD functions
# The API used in this test is V1, which will be obsolete and we will need update later

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
def read_project(login_session_id, user_id):
   
    #1374 is case "Enron Summit 2024" in consulting
    search_url = baseurl + "/rest/api/v2/projects/1819?userId=" + str(user_id);

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
    payload = {
    }

    # Send POST request to retrieve projects
    response = requests.get(search_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response to get project list
    response_data = response.json()
    fields_count = sum(len(item.get("fields", [])) for item in response_data)

    if fields_count == 2:
        print(f"returned " + str(fields_count) + " fields.")
        print(response_data[0]["fields"][0]["fieldValue"])
    else:
        print("Call failed.")
    
# Main Execution
try:
    # Step 2: Authenticate to get session ID and user ID
    #session_id, user_id = authenticate(username, password)
    session_id = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6dUExTTBVblF2akg3Y0tvbzBuSFZDcWFzY3NWNFhPTTBoUTJOR0ZvWU00In0.eyJleHAiOjE3NDI0ODIwMjAsImlhdCI6MTc0MjQ4MTcyMCwianRpIjoiZWFjMjRkYjItOGU1Yy00NzdjLWJiZGUtMjYwOGVmY2RkZDg2IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnVzLWVhc3QtMS5yZXZlYWwtZ2xvYmFsLmNvbS9yZWFsbXMvODEwMTAwMDIiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiOTg4NTEyN2ItNGQyYS00ZWFlLWIxOTQtMTI4M2YzZDE0ZjkzIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiUmV2ZWFsUmVzdEFQSSIsInNpZCI6IjNmNmNmZDZmLWQ5ZjktNDlhYS1iYzJmLTljZjJlNjcwYjNiYiIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLTgxMDEwMDAyIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoiZ3JvdXBzX3Njb3BlIHByb2ZpbGUgZW1haWwgb3BlbmlkIFJldmVhbE5vUGFzc3dvcmRDaGFuZ2UiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZ3JvdXBzX2NsYWltIjpbIi9OZXhMUFN0b3J5Ym9va3MvMTAwMzk4MCIsIi9SZXZpZXdQcm9qZWN0cy9NU0E4MTAxMDAwMi0xMzA0IiwiL1Jldmlld1Byb2plY3RzL01TQTgxMDEwMDAyLTEzNzQiLCIvUmV2aWV3UHJvamVjdHMvTVNBODEwMTAwMDItMTgxMCIsIi9SZXZpZXdQcm9qZWN0cy9NU0E4MTAxMDAwMi0xODE5IiwiL1Jldmlld1Byb2plY3RzL01TQTgxMDEwMDAyLTE4NDQiLCIvUmV2aWV3UHJvamVjdHMvTVNBODEwMTAwMDItMTk4MiJdLCJuYW1lIjoibmV4bHAgd2luZHkiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJuZXhscCIsImdpdmVuX25hbWUiOiJuZXhscCIsImZhbWlseV9uYW1lIjoid2luZHkiLCJlbWFpbCI6Im5leGxwLmNoaWNhZ29AZ21haWwuY29tIn0.YXXe3O1YsfDsrfPJTVVMM6oyY7OFAbUJFAxhw-AKfHZ-GRBT7umIklLvo0bJ6tRZyEUGgsvQaOscHD0CALepeDxzav0Jz9GCxnpbGuLiANJTFGc4gruHsu0QjvUu7QHHo30S16ClE4gTudoqBzjfBT7oNuafOmytNN82a1J0ea3CQPMR6RnprODX0zP8wO89Qeh-kWSNW6HVExs-sbDZYnm8jm7if1jI82qIuoVVzNWfFnAXFecDA5IbKZnxzk7L-9j8S5NLZF-S598UCb3HILE2ICPY79RHe4772rCELPKBgDZHoWIl4pjCLj4Tdc3vQLEXAZ6tNxQ7HAXz31SyjW_6QhgDCPHHzBa-6WIik5_ryMBX4A9bErDk3KfdGerCx_An5-W9zjcDFOG5foOZDF_WYZvzZcLX6irM7378i8u2xu3xAKYAC5fv_54jAT4LHUaD3wC7BfnAzzXf_SUC4VyiwTpli5SxNqv57yn1q73xYwtqFwTXVLLC5knyoizMqn61iGC68DQi6blY9eHe6klV5SbzPlOXX3xShmACXveu7mFJ13P_vsRDrLc-jKRuKtbunsfJqLSr0XSUD0WWnoh1oSMCQjgpoLJLwFV_310BaENEdqmmABSU_xGR9fuXnioKZITJMI8brE8V4BJjdWDOApclBebtbQON0lnTXHE'
    user_id = 526
    # Step 3: read Body Text back
    read_project(session_id, user_id)

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")