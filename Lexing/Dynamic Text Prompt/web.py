from flask import Flask, render_template, request,jsonify
from Tracking import get_walking_directions
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
api_key = "AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8"
origin_lat = 51.455205632789955
origin_lng = -2.582902280206153
destination_lat = 51.454514
destination_lng = -2.587910

I,D,S = get_walking_directions(api_key, origin_lat, origin_lng, destination_lat, destination_lng)
print(I)
print(S[0]['lat'])


@app.route('/')
def index():
    return render_template('maps.html')


@app.route('/update_location', methods=['POST'])
def receive_data():
    # Receive latitude and longitude data from the AJAX request
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']

    # Perform any processing you want with the latitude and longitude values
    print("Received latitude:", latitude)
    print("Received longitude:", longitude)

    closest_instruction,coords = find_closest_instruction(latitude, longitude, S,I)
    distance_to_instruction = calculate_distance(latitude, longitude, coords[0],
                                                     coords[1])
    prompt = f"Next instruction: {closest_instruction}. Distance: {distance_to_instruction} km"

    print(prompt)
    # Return latitude and longitude as a JSON response
    return jsonify({"latitude": latitude, "longitude": longitude})

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def find_closest_instruction(current_lat, current_lon, instructions,words):
    min_distance = float('inf')
    closest_instruction = None
    count = 0


    for instruction in instructions:

        distance = calculate_distance(current_lat, current_lon, instruction['lat'], instruction['lng'])
        if distance < min_distance:
            min_distance = distance
            closest_instruction = words[count]
            coords = (instruction['lat'],instruction['lng'])

        count += 1

    return closest_instruction,coords



if __name__ == '__main__':
    app.run(debug=True)




