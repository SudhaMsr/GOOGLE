from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_location', methods=['POST'])
def update_location():

    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Process or store the location data as needed.

    return 'Location updated successfully.'


if __name__ == '__main__':
    app.run(debug=True)
