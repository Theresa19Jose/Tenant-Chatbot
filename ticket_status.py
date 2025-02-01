import requests
from api.auth import get_auth_token
from config import auth_api, USERNAME, PASSWORD, premises_url

def get_ticket_status(ticket_number):
    token = get_auth_token(auth_api, USERNAME, PASSWORD)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    url = enter your url
    
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
