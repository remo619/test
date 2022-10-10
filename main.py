from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from datetime import datetime as dt
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.camera import Camera
import numpy as np
from kivy.graphics.texture import Texture
import cv2

from object_det import *
from distance_estimation import *
from say import *

"""
class Distance(MDWidget):
    def __init__(self,**kwargs):
        super(Distance, self).__init__(**kwargs)
        self.text = "say(data)"
"""

class AndroidCam(Camera):
    resolution = w,h =(640,480)
    text = "..."
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
                return
            frame = np.fromstring(buf, 'uint8').reshape(self.w, self.h)
            frame = cv2.cvtColor(frame, 93) #YUV to BGR NV21
        else:
            ret, frame = self._camera._device.read()
            #cv2.imshow(f"{}")
        self.pre_process_frame(frame)
        self.process_frame(self.frame)
        self.display_frame()

    def pre_process_frame(self,frame):
        frame = np.flip(frame, 0)
        frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
        self.frame = frame

    #Object detection
    def process_frame(self, frame):
        result, rectangles, class_names, data_list = detect(frame)
        self.data_list = data_list
        self.frame = result

    def get_distance(self):
        data = distance_estimation(self.frame,self.data_list)
        self.text = say(data)

    def display_frame(self):
        buf = self.frame.tobytes()
        self.texture = Texture.create(size=np.flip(self.resolution), colorfmt='rgba')
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')


class CamApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        Screen = Builder.load_file("GUI.kv")
        return Screen

    def on_start(self, **kwargs):
        if platform=="android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])

    def close_application(self):
        MDApp.get_running_app().stop()
        Window.close()

if __name__ == '__main__':
    CamApp().run()
