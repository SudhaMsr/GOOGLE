from flask import Flask, render_template, request,jsonify

app = Flask(__name__)

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
    # For demonstration, let's just print them
    print("Received latitude:", latitude)
    print("Received longitude:", longitude)

    # You can also return a response to the JavaScript code if needed
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True)
