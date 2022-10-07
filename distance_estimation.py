from object_det import detect
import cv2
import numpy as np
known_distance = 100 #CM
person_width = 45 #CM
cellphone_width = 7.5 #CM
chair_width = 56
backpack_width =1
bottle_width = 8.5
laptop_width =42
keyboard_width =43.5
#bicycle_width = 1
#car_width = 1
#motorbike_width = 1


# colors for object detected
COLORS = [(255,0,0),(255,0,255),(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN =(0,255,0)
BLACK =(0,0,0)
# defining fonts
FONTS = cv2.FONT_HERSHEY_COMPLEX

'''measured_distance = known_distance
   width_in_rf = width detected by obj_detection'''

def focal_length_finder (measured_distance, real_width, width_in_rf):
    focal_length = (width_in_rf * measured_distance) / real_width

    return focal_length

# distance finder function
def distance_finder(focal_length, real_object_width, width_in_frame):
    distance = (real_object_width * focal_length) / width_in_frame
    #print(distance)
    return int(distance)

def width_in_rf(x):
    img = cv2.imread(f"images/ref/{x}.jpg")
    img = cv2.resize(img,(640,480))
    #print("width"+x,detect(img)[3][0][1])
    return detect(img)[3][0][1]


def distance_estimation(img, data):
    focal_person = focal_length_finder(known_distance, person_width, width_in_rf("person"))
    focal_laptop = focal_length_finder(known_distance, laptop_width, width_in_rf("laptop"))
    focal_chair = focal_length_finder(known_distance, chair_width, width_in_rf("chair"))
    focal_bottle = focal_length_finder(known_distance, chair_width, width_in_rf("bottle"))

    for d in data:
        if d == []:
            break
        elif d[0] =='person':
            distance = distance_finder(focal_person, person_width, d[1])
            x, y = d[2]
            d.append(distance)
        elif d[0] =='laptop':
            distance = distance_finder (focal_laptop, laptop_width, d[1])
            x, y = d[2]
            d.append(distance)
        elif d[0] =='bottle':
            distance = distance_finder (focal_bottle, bottle_width, d[1])
            x, y = d[2]
            d.append(distance)
        elif d[0] == 'chair':
            distance = distance_finder (focal_chair, chair_width, d[1])
            x, y = d[2]
            d.append(distance)
        cv2.rectangle(img, (x, y-3), (x+150, y+23),BLACK,-1 )
        cv2.putText(img, f'Dis: {int(distance)} cm', (x+5,y+13), FONTS, 0.48, GREEN, 1)
    return data
