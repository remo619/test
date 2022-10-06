from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from datetime import datetime as dt
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
import cv2
if platform=="android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])

class AndroidCam(Camera):
    camera_resolution = (640,480)

    def _camera_loaded(self, *largs):
        self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgb')
        self.texture_size = list(self.texture.size)

    def on_tex(self, *l):
        super(AndroidCam, self).on_tex(*l)
        if self._camera._buffer is None:
            return None
        frame = self.frame_from_buf()
        self.frame_to_screen(frame)


    def frame_from_buf(self):
        w, h = self.resolution
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))
        #frame_bgr = cv2.cvtColor(frame, 93)
        return frame

    def frame_to_screen(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tostring()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')


class CamApp(MDApp):
    def build(self):
        #Window.size= [300,600]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        Screen = Builder.load_file("GUI.kv")
        return Screen
    def close_application(self):
        # closing application
        MDApp.get_running_app().stop()
        # removing window
        Window.close()
if __name__ == '__main__':
    CamApp().run()
