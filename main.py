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
import numpy as np
from kivy.logger import Logger
from kivy.graphics.texture import Texture
import cv2
if platform=="android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA
        #Permission.WRITE_EXTERNAL_STORAGE,
        #Permission.READ_EXTERNAL_STORAGE
    ])

class AndroidCam(Camera):
    resolution = w,h =(640,480)

    def __init__(self,**kwargs):
        super(AndroidCam,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_texture, 1.0 /30.0)
    def _camera_loaded():
        if platform == "android":
            self.texture = Texture.create(size=self.resolution, colorfmt='rgba')
            self.texture_size = list(self.texture.size)
        else:
            self.texture = self._camera.texture
            self.texture_size = list(self.texture.size)

    def update_texture(self,*l):
        if platform == 'android':
            buf = self._camera.grab_frame()
            if buf is None:
                Logger.info("Camera: No valid frame")
                return
            frame = np.fromstring(buf, 'uint8').reshape(self.h + self.h // 2, self.w)
            frame = cvtColor(frame, 93)
            Logger.info(f"Camera: update texture")
        else:
            frame = self._camera._device.read()
        #self.extract_frame()
        self.process_frame(frame)
        self.display_frame()

    #def extract_frame(self):
        #self.frame = np.frombuffer(self.frame, np.uint8)
        #self.frame = self.frame.reshape((self.w,self.h, 4))
    def process_frame(self,frame):
        self.frame = np.flip(frame, 0)
    def display_frame(self):
        buf = self.frame.tobytes()
        self.texture = Texture.create(size=np.flip(self.resolution), colorfmt='rgb')
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')


class CamApp(MDApp):
    def build(self):
        #Window.size= [300,600]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        Screen = Builder.load_file("GUI.kv")
        return Screen
    def close_application(self):
        MDApp.get_running_app().stop()
        Window.close()
        Logger.info("Application Closed")

if __name__ == '__main__':
    CamApp().run()
