import objc
from Foundation import *
from CoreLocation import *


# Define a function to handle location updates
def location_update(manager, locations):
    for location in locations:
        print("Latitude:", location.coordinate().latitude)
        print("Longitude:", location.coordinate().longitude)


def main():
    # Create a CLLocationManager object
    locationManager = objc.lookUpClass('CLLocationManager').alloc().init()

    # Set the delegate for location updates
    locationManager.setDelegate_(None)
    locationManager.setDelegate_(location_update)

    # Request authorization from the user
    locationManager.requestAlwaysAuthorization()

    # Start updating location
    locationManager.startUpdatingLocation()

    # Run the main event loop
    objc.lookUpClass('NSRunLoop').currentRunLoop().run()


if __name__ == "__main__":
    print("hello")
    main()