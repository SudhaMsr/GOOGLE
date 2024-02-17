from flask import Flask, render_template, request
from flask_socketio import SocketIO
from math import radians, sin, cos, sqrt, atan2
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "thesecretkey"
socketio = SocketIO(app)

api_key = "AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8"

latitude, longitude = None, None
last_instruction = ""

destination_lat, destination_lng = 51.47517914572953, -0.18708572037465862


@app.route('/')
def index():
    return render_template('maps.html')


@app.route('/update_location', methods=['POST'])
def update_loc():
    global latitude, longitude
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    get_prompt(destination_lat, destination_lng)
    return "Location updated successfully!"


@socketio.on('update_prompt')
def get_prompt(destination_lat, destination_lng):
    global latitude, longitude

    I, D, S = get_walking_directions(api_key, latitude, longitude, destination_lat, destination_lng)
    # closest_instruction, coords = find_closest_instruction(latitude, longitude, S, I)
    closest_instruction = I[0]
    global last_instruction
    if closest_instruction == last_instruction:
        return
    last_instruction = closest_instruction

    # distance_to_instruction = calculate_distance(latitude, longitude, coords[0], coords[1])
    # prompt = f"Next instruction: {closest_instruction}. Distance: {distance_to_instruction} km"
    prompt = f"Next instruction: {closest_instruction}."
    print("sending message")
    socketio.send(prompt)


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
        return instructions, distances, start_locations


    else:
        print(f"Error: {data['status']}")


if __name__ == '__main__':
    socketio.run(app, debug=True)
