
import googlemaps

def getTextDirections():
    API_KEY = 'AIzaSyAj5is27Ui1bJ5CMSCdGEcus41LIiZ5Zy8'
    map_client = googlemaps.Client(API_KEY)

    source = "University of Bristol"
    destination = "Bristol Temple meads"

    direction_result = map_client.directions(source,destination,mode = "walking",step_by_step = True)

    print(direction_result[0]['legs'][0]['distance'])
    print(direction_result[0]['legs'][0]['duration'])

    for step in direction_result[0]['legs'][0]['steps']:
        print(step['html_instructions'])



getTextDirections()