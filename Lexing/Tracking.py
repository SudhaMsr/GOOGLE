
import requests
import time
import platform
import uuid
import subprocess
import re
import googlemaps
import geocoder



def get_current_loc(api_key,mac,ssid,signal_strength):
    url = 'https://www.googleapis.com/geolocation/v1/geolocate'
    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}

    t0 = time.time()
    wifiAccessPoints = {"macAddress": mac, "signalStrength": signal_strength, "ssid": ssid}
    print(wifiAccessPoints)
    request_data = {
            'considerIp': 'true',
            'wifiAccessPoints': wifiAccessPoints
        }

    response = requests.post(url, headers=headers, params=params, json=request_data)
    print(time.time() - t0)


    if response.status_code == 200:
            location = response.json()['location']
            acc = response.json()['accuracy']
            altitude = response.json().get('altitude')
            print(f'accuracy = {acc} and altitude ={altitude}')
            print(location["lat"], location["lng"])
            return location["lat"], location["lng"]
    else:
            print('Error:', response.status_code, response.text)

def reverse_geocode(api_key, latitude, longitude):
    geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'latlng': f'{latitude},{longitude}',
        'key': api_key
    }
    response = requests.get(geocoding_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        results = data['results']
        if results:u

            address_components = results[0]['address_components']
            for component in address_components:
                print(f"{component['types'][0]}: {component['long_name']}")
        else:
            print('No results found')
    else:
        print('Geocoding Error:', data['status'])


def get_mac_address():
    try:
        mac_address = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xFF) for elements in range(5, -1, -1)])
        return mac_address
    except Exception as e:
        print(f"Error: {e}")


def get_current_ssid():
    try:
        result = subprocess.run(
            ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
            capture_output=True, text=True, check=True)

        ssid_line = [line.strip() for line in result.stdout.splitlines() if line.strip().startswith("SSID:")][0]
        ssid = ssid_line.split(':', 1)[1].strip()

        signal_strength_line = \
        [line.strip() for line in result.stdout.splitlines() if line.strip().startswith("agrCtlRSSI:")][0]
        signal_strength = int(signal_strength_line.split(':', 1)[1].strip())

        return ssid,signal_strength

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")



if __name__ == "__main__":

        api_key = 'AIzaSyAvh4QL3ZYXkWGm6UQoeYmTOoLP6SksgVs'
        api_key2 = 'AIzaSyAfeVvRD0R0vm8tgrz7XfD5LWrOIWAe9KI'
        api_key3 = 'AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8'
        while True:
            m = get_mac_address()
            s,st = get_current_ssid()
            lat,lng = get_current_loc(api_key,m,s,st)
            reverse_geocode(api_key2,lat,lng)
            print('\n')


