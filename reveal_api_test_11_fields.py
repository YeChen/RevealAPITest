# This test script is used to test fields 
#  1. creation
#  2. add to profile 
#  3. update value (through bulkTag)
#  4. wait till job finishes, check field value 

import requests
import os
import time

# Step 1: setup, retrieve USER and PASSWORD secrets from Colab or os 
username = 'nexlp'
password = os.getenv('DEMO_PASSWORD')
baseurl = "https://consulting.us-east-1.reveal11.cloud"
caseid = 1819  #1819 is case "API test" in consulting
docids = [1]
fieldname = "TEXT_FIELD_08"
field_value_to_update = "hello world!"
default_fieldprofile_id = 1

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

# Step 2: create a text field
def create_field(login_session_id, field_name):
   
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

    #check if the field exists already
    search_url = baseurl + f"/rest/api/v2/{caseid}/fields?includeNotImportable=true&includeSpecial=true&start=0&count=2147483647"

    # Payload data
    payload = {}

    # Send POST request to retrieve projects
    response = requests.get(search_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the response to get project list
    response_data = response.json()

    field_exists = any(result['fieldName'].lower() == field_name.lower() for result in response_data['results'])

    if field_exists: 
        print(f"field:{field_name} exists, pass creation")
        for item in response_data.get("results", []):
                print(item.get("fieldName"))
                if item.get("fieldName").lower() == field_name.lower():
                    return item.get("fieldId")                                       
    else:
        #create field 
        print("create field")
        search_url = baseurl + f"/rest/api/v2/{caseid}/fields"
        payload = {
            "fieldId": 0,
            "fieldName": field_name,
            "displayName": field_name,
            "dataType": "nvarchar",
            "maxLength": 4000,
            "dataTypeDesc": "",
            "isTranscriptLookup": False,
            "isRelationalField": False,
            "isSearchable": True,
            "isUpdatable": True,
            "isProductionUpdatable": True,
            "isMultiValue": True,
            "isCustomField": True,
            "isImportable": True,
            "isNativeFileField": True,
            "isSortable": True,
            "isFacetable": True,
            "hasExactText": True,
            "indexed": True,
            "pinned": True,
            "stored": True,
            "type": "Text"
        }
        response = requests.post(search_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails
        response_data = response.json()
        if response_data["fieldId"]: 
            print("field created.")
            return response_data["fieldId"]

    #update 
    # URL: https://consulting.us-east-1.reveal11.cloud/rest/api/v2/1819/jobs/bulkTag
    # {"documentSelectionType":"Subset","selectedDocumentItemIds":[1,2,3,4],"updateFieldsEntry":{"variableSets":[{"fieldId":426,"variables":[{"displayOrder":0,"category":"UserText","value":"aaabbb"}]}],"updateOption":"KeepExisting"}}      

# Step 3: add to default profile
def add_to_profile(login_session_id, field_id):
   
    # Headers
    headers = {    
      "incontrolauthtoken": login_session_id,
      "Accept": "application/json", 
      "Accept-Encoding": "gzip, deflate, br, zstd",
      "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
      "Content-Length": "500",
      "Content-Type": "application/json-patch+json",
      "origin": baseurl,
      "priority": "u=1, i",
      "referer": baseurl + "/rest/api-docs/index.html?urls.primaryName=v2",
      "sec-ch-ua":'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
      "sec-ch-ua-platform":"Windows",
      "sec-fetch-mode": "cors", 
      "sec-fetch-site": "same-origin",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    #check if the field exists already
    add_field_url = baseurl + f"/rest/api/v2/{caseid}/fieldProfiles/{default_fieldprofile_id}/fields/add"

    # Payload data  
    payload = [
        {
            "fieldId": field_id,
            "isVisible": 1
        }
    ]

    # Send PUT request 
    response = requests.put(add_field_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    print("field added to default profile ")

# Step 4: update the text field value
def update_field_value(login_session_id, field_id, field_value):
   
    # Headers
    headers = {    
      "incontrolauthtoken": login_session_id,
      "Accept": "application/json", 
      "Accept-Encoding": "gzip, deflate, br, zstd",
      "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
      "Content-Length": "500",
      "Content-Type": "application/json-patch+json",
      "origin": baseurl,
      "priority": "u=1, i",
      "referer": baseurl + "/rest/api-docs/index.html?urls.primaryName=v2",
      "sec-ch-ua":'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
      "sec-ch-ua-platform":"Windows",
      "sec-fetch-mode": "cors", 
      "sec-fetch-site": "same-origin",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    #check if the field exists already
    bulktag_url = baseurl + f"/rest/api/v2/{caseid}/jobs/bulkTag"

    # Payload data  
    #{"documentSelectionType":"Subset","selectedDocumentItemIds":[2,1],"updateFieldsEntry":{"variableSets":[{"fieldId":428,"variables":[{"displayOrder":0,"category":"UserText","value":"cccddd"}]}],"updateOption":"Replace"}}
    payload = {
        "documentSelectionType": "Subset",
        "selectedDocumentItemIds": docids,
        "updateFieldsEntry": {
            "variableSets": [
                {
                    "fieldId": field_id,
                    "variables": [
                        {
                            "displayOrder": 0,
                            "category": "UserText",
                            "value": f"{field_value}"
                        }
                    ]
                }
            ],
            "updateOption": "Replace"
        }
    }

    #payload = "{\"documentSelectionType\":\"Subset\",\"selectedDocumentItemIds\":[1], \"name\": \"test\", \"updateFieldsEntry\":{\"variableSets\":[{\"fieldId\":426,\"variables\":[{\"displayOrder\":0,\"category\":\"UserText\",\"value\":\"hhh\"}]}],\"updateOption\":\"Replace\"}}"

    # Send POST request to retrieve projects
    response = requests.post(bulktag_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails

    print("job for update submitted.")
  
    return response.json()["jobId"]    

# Step 5: read the text field back and confirm it is updated
def confirm_field_value(login_session_id, job_id):
   
    # Headers
    headers = {    
      "incontrolauthtoken": login_session_id,
      "Accept": "application/json"
    }

    #check if job finished
    bulktagjob_url = baseurl + f"/rest/api/v2/{caseid}/jobs/bulkTag/{job_id}"
    response = requests.get(url=bulktagjob_url, headers=headers)
    response.raise_for_status()  # Raise an error if the request fails
    jobstatus = response.json()["status"]      
    trycount = 0 
    while jobstatus != "Complete" and trycount < 3: 
        time.sleep(10)
        trycount += 1
        response = requests.get(bulktagjob_url, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails
        jobstatus = response.json()["status"]       

    if (jobstatus == "Complete"):         
        search_url = baseurl + f"/rest/api/v2/{caseid}/search"
        # Payload data
        payload = {
            "queryString":"{\"type\":\"advancedBoolean\",\"clauses\":[{\"type\":\"termIn\",\"fieldName\":\"ITEMID\",\"values\":[\"" + f"{docids[0]}" + "\"],\"exact\":true}],\"operations\":[]}",
            "queryType":"Bql",
            "documentCriteria":{"start":0,"count":25,"fieldProfileId":default_fieldprofile_id}
        }
        # Send GET request to retrieve projects
        response = requests.post(search_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the response to get project list
        search_response = response.json()
        text_found = search_response["documentResults"]["documents"][0]["fields"][fieldname]

        if text_found[0] == field_value_to_update:
            print("Confirmed the value is set properly.")
        else:
            print("failed to confirm the result is saved. field has value: " + text_found)
    
    else: 
        print("Update didn't succeed. Check later.")  
    
# Main Execution
try:
    # Step 1: Authenticate to get session ID and user ID
    session_id, user_id = authenticate(username, password)

    # Step 2: create new field  
    field_id = create_field(session_id, fieldname)

    # Step 3: add field to default profile 
    # NOTICE!!! field won't read/update if it is not in profile
    add_to_profile(session_id, field_id) 

    # Step 4:  
    job_id = update_field_value(session_id, field_id, field_value_to_update)

    # Step 5: serach and confirm field value is updated   
    confirm_field_value(session_id, job_id)
 

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Error: {e}")