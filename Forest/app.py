from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import pyobjus
from pyobjus.dylib_manager import load_framework, INCLUDE
load_framework(INCLUDE.Appkit)
from pyobjus import autoclass, PythonClass

Builder.load_string('''
<CameraApp>:
    orientation: 'vertical'
    CameraWidget:
        id: camera_widget
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_release: app.capture()
''')

class CameraWidget(Image):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self._capture = None

    def start(self, capture_callback):
        self._capture = autoclass('AVCaptureSession').alloc().init()
        device = autoclass('AVCaptureDevice').defaultDeviceWithMediaType_('vide')
        input = autoclass('AVCaptureDeviceInput').deviceInputWithDevice_error_(device, None)
        if input:
            self._capture.addInput_(input)
        else:
            print("Error: could not create AVCaptureDeviceInput")

        output = autoclass('AVCaptureVideoDataOutput').alloc().init()
        queue = autoclass('dispatch').get_global_queue(0, 0)
        output.setSampleBufferDelegate_queue_(capture_callback, queue)
        self._capture.addOutput_(output)
        self._capture.startRunning()

class CameraApp(App):
    def build(self):
        self.capture = None
        self.camera = CameraWidget()
        return BoxLayout(orientation='vertical', children=[self.camera])

    def on_start(self):
        self.capture = CameraCapture(self.camera.texture)
        self.camera.start(self.capture.capture_callback)

class CameraCapture(PythonClass):
    def __init__(self, texture):
        super(CameraCapture, self).__init__()
        self.texture = texture

    def capture_callback(self, sample_buffer, connection):
        self.texture.handle_video_frame(sample_buffer)

if __name__ == '__main__':
    CameraApp().run()
