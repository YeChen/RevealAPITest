# This test script is used to test Project CRUD functions
# The get_projects read back all projects and returns a non-existent project name for creation 
# The project will then be created, updated and deleted  

import requests
import os

# Step 1: setup, retrieve USER and PASSWORD secrets from Colab or os 
#username = userdata.get("DEMO_USER")
#password = userdata.get("DEMO_PASSWORD")
username = 'nexlp'
password = os.getenv('DEMO_PASSWORD')
baseurl = "https://consulting.us-east-1.reveal11.cloud"
test_project_prefix = 'APITest_'
clientid = 84 #APIClient
companyid = 70 #API

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
def get_projects(login_session_id, user_id):
    """
    Retrieves a list of projects for the authenticated user and prints each project name.
    """
    projects_url = baseurl + "/rest/api/v2/projects"

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
    response = requests.get(projects_url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response to get project list
    projects_response = response.json()
    projects = projects_response.get("results", [])

    # Print each project name
    if projects:
        print("Project Names:")
        for project in projects:
            print(project.get("projectName", "Unnamed Project"))

        existing_names = {project["projectName"] for project in projects}
        number = 1
        while f"{test_project_prefix}{number}" in existing_names:
            number += 1
        return f"{test_project_prefix}{number}"    
    else:
            print("No projects found.")

# Step 4: create project
def create_project(login_session_id, project_name):

  # Endpoint URL
  url = baseurl + "/rest/api/v2/projects"

  # Payload data
  payload = {
      "projectName": project_name,
      "projectDbId": project_name,
      "companyId": companyid, #Company: API, use 1 if we want to test company "Reveal" 
      "clientId": clientid, #ClientName: APIClient, use 1 if we want to test client "Reveal"
      "timezone": "UTC"
  }

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

  try:
      # Send POST request
      response = requests.post(url, json=payload, headers=headers)

      # Check if the request was successful
      if response.status_code == 202:
          print("Project " + project_name + " created successfully!")
          print("Response Data:", response.json())
          return response.json().get("id"); 
      else:
          print(f"Failed to create project. Status Code: {response.status_code}")
          print("Response:", response.text)

  except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")

# Step 5: update project
# Note: has to use an admin account
def update_project(login_session_id, projectid, project_name_new):

  # Endpoint URL
  url = baseurl + "/rest/api/v2/projects/" + str(projectid)

  # Payload data
  payload = {
    "projectName": project_name_new,
    "hasDocumentLevelSecurity": "true",
    "isProjectTemplate": "true",
    "isFavorite": "true",
    "isDeactivated": "true",
    "isAskEnabledExternally": "true",
    "clientNumber": "null",
    "matterNumber": "null"
  }

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

  try:
      # Send POST request
      response = requests.patch(url, json=payload, headers=headers)

      # Check if the request was successful
      if response.status_code == 204:
          print("Project " + project_name_new + " updated successfully!")        
      else:
          print(f"Failed to update project. Status Code: {response.status_code}")
          print("Response:", response.text)

  except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")



# Main Execution
try:
    # Step 2: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 3: Retrieve new project name to use
    project_to_create = get_projects(session_id, user_id)

    # Step 4: create
    project_created_id = create_project(session_id, project_to_create)

    # Step 5: update 
    update_project(session_id, project_created_id, project_to_create + "_updated") 

    # Step 6: delete 
    # FUNCTION MISSING

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")