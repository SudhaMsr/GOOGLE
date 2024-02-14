from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import gps


class GPSDemo(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gps_location = None
        self.gps_status = None

        gps.configure(on_location=self.on_location, on_status=self.on_status)
        Clock.schedule_once(self.start_gps, 1)

    def start_gps(self, dt):
        gps.start()

    def stop_gps(self):
        gps.stop()

    def on_location(self, **kwargs):
        self.gps_location = kwargs['lat'], kwargs['lon']
        print("GPS Location:", self.gps_location)

    def on_status(self, stype, status):
        self.gps_status = status
        print("GPS status:", self.gps_status)


class MyApp(App):
    def build(self):
        return GPSDemo()


if __name__ == '__main__':
    MyApp().run()