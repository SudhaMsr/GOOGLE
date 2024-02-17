import requests

def get_walking_directions(api_key, origin_lat, origin_lng, destination_lat, destination_lng):
    origin = f"{origin_lat},{origin_lng}"
    destination = f"{destination_lat},{destination_lng}"
    instructions = []
    start_locations = []
    distances = []

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=walking&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":

        steps = data["routes"][0]["legs"][0]["steps"]
        for step in steps:
            instruction = step["html_instructions"]
            distance = step["distance"]["text"]
            start_location = step["start_location"]
            end_location = step["end_location"]
            instructions.append(instruction)
            distances.append(distance)
            start_locations.append(start_location)
        return instructions,distances,start_locations


    else:
        print(f"Error: {data['status']}")

# Replace these values with your Google Maps API key and latitude/longitude coordinates




