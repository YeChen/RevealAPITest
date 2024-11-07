import requests
import os

# Step 1: Retrieve USER and PASSWORD secrets from Colab
#username = userdata.get("DEMO_USER")
#password = userdata.get("DEMO_PASSWORD")
username = 'nexlp'
password = os.getenv('DEMO_PASSWORD')

if not username or not password:
    raise ValueError("Secrets USER and PASSWORD must be set in Colab.")

# Step 2: Define the authentication function
def authenticate(username, password):
    """
    Authenticates with the Reveal API using username and password.
    Returns loginSessionId and userId if authentication is successful.
    """
    login_url = "https://consulting.us-east-1.reveal11.cloud/rest/api/v2/login"
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
    projects_url = "https://consulting.us-east-1.reveal11.cloud/rest/api/v2/projects"

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
    else:
        print("No projects found.")

# Step 4: Define the function to retrieve projects
def create_project(login_session_id, user_id):

  # Endpoint URL
  url = "https://consulting.us-east-1.reveal11.cloud/rest/api/v2/projects"

  # Payload data
  payload = {
      "projectName": "APITest005",
      "projectDbId": "apitest005",
      "companyId": 1,
      "clientId": 1,
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
      "origin": "https://consulting.us-east-1.reveal11.cloud",
      "priority": "u=1, i",
      "referer": "https://consulting.us-east-1.reveal11.cloud/admin/companies/1/projects",
      "sec-ch-ua":'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
      "sec-ch-ua-platform":"Windows",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
  }

  try:
      # Send POST request
      response = requests.post(url, json=payload, headers=headers)

      # Check if the request was successful
      if response.status_code == 202:
          print("Project created successfully!")
          print("Response Data:", response.json())
      else:
          print(f"Failed to create project. Status Code: {response.status_code}")
          print("Response:", response.text)

  except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")


# Main Execution
try:
    # Step 2: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 3: Retrieve and print project names
    get_projects(session_id, user_id)

    # Step 4: create
    create_project(session_id, user_id)

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")