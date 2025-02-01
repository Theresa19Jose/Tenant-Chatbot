# media_request_api.py
import requests

def upload_media(file_path, domain, requst_number):
    url = "http://192.168.0.214:5001/upload-media"  # Replace with your actual Flask API URL

    # Construct the desired file path for the service request
    # request_file_path = f"serviceRequests\\{domain}\\{requst_number}"
    # request_file_path = f"serviceRequests\\{domain}\\{requst_number}"

    # Open the image file in binary mode
    with open(file_path, "rb") as media_file:
        print(media_file)
        # Prepare the files dictionary to send with the POST request
        files = {
            "media": media_file
        }
        # Prepare the data dictionary to send with the POST request
        data = {
            # "filePath": request_file_path,
            "domain": domain,
            "requst_number": requst_number
        }

        # Send the POST request
        response = requests.post(url, files=files, data=data)
        print(f"Response content: {response.content}") 
    # Return the response status
    return response.status_code == 200, response.json()  # Return a tuple of success status and response data

