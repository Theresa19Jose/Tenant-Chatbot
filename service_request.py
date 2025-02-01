import requests
from api.auth import get_auth_token
from config import  auth_api, USERNAME, PASSWORD, service_api


import requests
from api.auth import get_auth_token
from config import auth_api, USERNAME, PASSWORD, service_api


def service_request(payload):
    try:
        # Get authentication token
        token = get_auth_token(auth_api, USERNAME, PASSWORD)
        print(token)
        
        # Set headers with Bearer token
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        
        # Make POST request with payload
        response = requests.post(service_api, headers=headers, json=payload)
        
        # Check response status code
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            ticket_number = response_data.get("serviceTicketNumber", "")
            request_number = response_data.get("requestNumber", " ")
            print(f"Service request successful. Ticket number: {ticket_number}")
            return ticket_number , request_number
        else:
            print(f"Service request failed. Status code: {response.status_code}")
            return ""
    
    except Exception as e:
        print(f"Exception occurred during service request: {e}")
        return ""

    