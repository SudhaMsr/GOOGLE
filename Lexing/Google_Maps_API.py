
import googlemaps
import time

def getTextDirections(source,destination):
    API_KEY = 'AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8'
    map_client = googlemaps.Client(API_KEY)

    source = source
    destination = destination

    t0 = time.time()
    direction_result = map_client.directions(source,destination,mode = "walking")
    print(time.time() - t0)

    print(direction_result[0]['legs'][0]['distance'])
    print(direction_result[0]['legs'][0]['duration'])

    for step in direction_result[0]['legs'][0]['steps']:
        print(step['html_instructions'])



getTextDirections("Print hall student accomodation","Physics building university of bristol")