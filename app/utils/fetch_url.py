import requests
import os


def fetch_url(url, params={}):
    # Headers including the authorization token
    auth_token = os.getenv("FIREANT_TOKEN")
    headers = {"Authorization": f"{auth_token}"}

    try:
        # Make the GET request
        response = requests.get(url, params, headers=headers)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Return the JSON response if the request was successful
        return response.json()

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
