import requests


def get_auth_token(api_login, username , password):
    headers = {
     'Content-Type': 'application/json'
    }

    params ={
         'userName' : username,
         'password' : password
    }

    auth_response = requests.post(api_login , headers=headers, json=params)

    if auth_response.status_code == 200:
         auth_data = auth_response.json()
         TOKEN = auth_data.get('accessToken')
         return  TOKEN
