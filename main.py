from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from datetime import datetime as dt
from kivy.clock import Clock
from kivy.lang import Builder
#from kivy.uix.camera import Camera
import numpy as np
from kivy_garden.xcamera import XCamera
from kivy.graphics.texture import Texture
import cv2
if platform=="android":
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])

class AndroidCam(XCamera):
    camera_resolution = w,h =(640,480)

    def __init__(self,**kwargs):
        super(AndroidCam,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_texture, 1.0 /30.0)

    def get_img(self,*l):
        #print(self._camera._update)
        #self._camera._update
        self.image_bytes = self._camera.texture.pixels
        return self.image_bytes

    def update_texture(self,dt):
        if type(self.get_img()) == bool:
            return
        self.extract_frame()
        self.process_frame()
        self.display_frame()

    def extract_frame(self):
        self.frame = np.frombuffer(self.get_img(), np.uint8)
        self.frame = self.frame.reshape((w, h, 4))


    def process_frame(self):
        self.frame = np.flip(self.frame, 0)

    def display_frame(self):
        buf=self.frame.tostring()
        self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgba')
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')


class CamApp(MDApp):
    def build(self):
        #Window.size= [300,600]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        Screen = Builder.load_file("GUI.kv")
        return Screen
    def close_application(self):
        # closing applicatio
        MDApp.get_running_app().stop()
        Window.close()
if __name__ == '__main__':
    CamApp().run()
