import requests
from api.auth import get_auth_token
from config import  auth_api, USERNAME, PASSWORD, userdata_api


def get_user_info(contact):

    token =  get_auth_token(auth_api, USERNAME, PASSWORD)
    print(token)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    params = {
        "contactNumber": contact
    }


    response = requests.post(userdata_api, headers=headers, json=params)
    user_data = response.json()
    user_name =  user_data["items"][0]["name"]
    reference_id = user_data['items'][0]['referenceId']
    return user_name , reference_id
   

   
    