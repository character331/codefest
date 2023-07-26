import requests
import random

# Set the API endpoint and parameters
api_endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
api_key = "AIzaSyCIE914GIf31hmI3aSFSGSMk0ZKFoGXTkw" # Replace with your actual API key


def get_geo(location):
    # Set the request parameters
    params = {
        "address": location,
        "key": api_key
    }

    # Send the request to the API
    response = requests.get(api_endpoint, params=params).json()

    # Extract the latitude and longitude from the API response
    try:
        lat = response["results"][0]["geometry"]["location"]["lat"] + random.randint(1, 100) * 0.001
        lng = response["results"][0]["geometry"]["location"]["lng"] + random.randint(1, 100) * 0.001
        return (lat, lng)
    except (IndexError, KeyError):
        print(f"Failed to get geolocation for '{location}'")
        return False