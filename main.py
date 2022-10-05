from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime as dt
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics.texture import Texture
import cv2
if platform=="android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(MDApp):
    def build(self):
        Window.size= [300,600]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        Screen = Builder.load_file("GUI.kv")
        Screen.add_widget(self.my_camera,2)
        return Screen

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
