
import requests

api_key = "AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8"

def geocode(address,api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        return "No location found"

if __name__ == '__main__':
    print(geocode("University of Bristol",api_key))