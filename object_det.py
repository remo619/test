import tflite_runtime.interpreter as tflite
import cv2
import numpy as np

def ReadLabelFile(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    ret = {}
    i=0
    for line in lines:
        #pair = line.strip().split(maxsplit=1)
        ret[i]=line.strip()
        i+=1
        #ret[int(pair[0])] = pair[1].strip()
    return ret

#model = "models/mobilenet_v2.tflite"
model = "models/detect.tflite"
#model = "models/ssd_mobilenet.tflite"
#model = "models/efficientdet_lite2.tflite"

labels =  ReadLabelFile("models/coco_labels.txt")
normalSize = (640, 480)

def detect(img):
    interpreter = tflite.Interpreter(model, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    picture = cv2.resize(img, (width, height))

    floating_model = False
    if input_details[0]['dtype'] == np.float32:
        floating_model = True


    initial_w, initial_h = normalSize

    input_data = np.expand_dims(picture, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    detected_boxes = interpreter.get_tensor(output_details[0]['index'])
    detected_classes = interpreter.get_tensor(output_details[1]['index'])
    detected_scores = interpreter.get_tensor(output_details[2]['index'])
    num_boxes = interpreter.get_tensor(output_details[3]['index'])

    rectangles = []
    class_names = []
    #object_data ={}
    data_list=[]
    for i in range(int(num_boxes)):
        bottom,left, top, right = detected_boxes[0][i]
        classId = int(detected_classes[0][i])
        score = detected_scores[0][i]
        if score > 0.4:
            xmin = left * initial_w
            ymin = bottom * initial_h
            xmax = right * initial_w
            ymax = top * initial_h
            box = [xmin, ymin, xmax, ymax]
            box = [int(i) for i in box]
            #data_list.append([class_names[classid], box[2], (box[0], box[1]-2)])
            rectangles.append(box)
            class_names.append(labels[classId])
            #classIds.append(classId)
            #object_data[classId] = [labels[classId]]
            #object_data[classId].extend(box)
            if classId ==0: # person class id
                data_list.append([labels[classId], box[2], (box[0], box[1]-2)])
            elif classId ==76:
                data_list.append([labels[classId], box[2], (box[0], box[1]-2)])
            elif classId ==72:
                data_list.append([labels[classId], box[2], (box[0], box[1]-2)])
            elif classId ==61:
                data_list.append([labels[classId], box[2], (box[0], box[1]-2)])
            cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]), (10, 255, 0), 2)
            label = '%s: %d%%' % (labels[classId], int(score*100))
            #print(data_list)
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, 0.48, 1)
            label_ymin = max(int(ymin), labelSize[1]+10)
            cv2.rectangle(img, (int(xmin), label_ymin-3), (int(xmin)+150, int(ymin)-23),(0,0,0),-1 )
            cv2.putText(img, label, (int(xmin), label_ymin-7), cv2.FONT_HERSHEY_COMPLEX, 0.48, (255, 255, 225), 1)


    return img, rectangles, class_names, data_list
