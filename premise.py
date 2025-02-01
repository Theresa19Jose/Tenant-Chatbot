import requests
from api.auth import get_auth_token
from config import auth_api, USERNAME, PASSWORD, premises_url

def get_premise(reference_id):
    print(reference_id)
    token = get_auth_token(auth_api, USERNAME, PASSWORD)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    params = {
        'referenceNumber': reference_id
    }

    try:
        response = requests.post(premises_url, headers=headers, json=params)
        if response.status_code == 200:
            premise_data = response.json()
            if isinstance(premise_data, list) and len(premise_data) > 0:
                premises = []
                for item in premise_data:
                    name = item.get("name", "")
                    address = item.get("address", "")
                    domain = item.get("domain", "")
                    identifier = item.get("identifier", "")
                    print(name)
                    print(address)
                    print(identifier)
                    print(domain)
                    premises.append({
                        "name": name,
                        "address": address,
                        "domain": domain,
                        "identifier": identifier
                    })
                return premises
            else:
                print("Error: No premises found in API response.")
                return None
        else:
            print(f"Error: Failed to retrieve premises. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception in API call: {e}")
        return None
