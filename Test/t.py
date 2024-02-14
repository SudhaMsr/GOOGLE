import requests

def get_walking_directions(api_key, origin_lat, origin_lng, destination_lat, destination_lng):
    origin = f"{origin_lat},{origin_lng}"
    destination = f"{destination_lat},{destination_lng}"

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=walking&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        steps = data["routes"][0]["legs"][0]["steps"]
        for step in steps:
            instruction = step["html_instructions"]  # HTML instruction, may contain tags
            distance = step["distance"]["text"]
            print(f"{instruction} ({distance})")
    else:
        print(f"Error: {data['status']}")

# Replace these values with your Google Maps API key and latitude/longitude coordinates
api_key = "AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8"
origin_lat = 40.748817  # Example latitude for Central Park, New York
origin_lng = -73.985428  # Example longitude for Central Park, New York
destination_lat = 40.758896  # Example latitude for Times Square, New York
destination_lng = -73.985130  # Example longitude for Times Square, New York

get_walking_directions(api_key, origin_lat, origin_lng, destination_lat, destination_lng)
