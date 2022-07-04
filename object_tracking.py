import os

import cv2
import numpy as np
from detection import ObjectDetection
import math

# Initialisation de la dectection d'Objet
od = ObjectDetection()

cap = cv2.VideoCapture("cars.mp4")

# initialiser un count
count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break

    # Cadre courant
    center_points_cur_frame = []

    # Detecter l'objet d'un cadre
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        center_points_cur_frame.append((cx, cy))
        #print("FRAME N°", count, " ", x, y, w, h)

        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # comparaison du cadre precedent et courant
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # maj de la position de l'ID
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue

            # retire les IDs des vehicules hors vision
            if not object_exists:
                tracking_objects.pop(object_id)

        # Ajout des IDS des noveaux vehicules détecté
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)

    print("Tracking objects")
    print(tracking_objects)


    print("CUR FRAME LEFT PTS")
    print(center_points_cur_frame)


    cv2.imshow("Frame", frame)


    center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
# print(count)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def object_dection(cap, od):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        center_points_cur_frame = []

        (class_ids, scores, boxes) = od.detect(frame)
        for box in boxes:
            (x,y,w,h)=box
            cx = int((x + x + w) / 2)
            cy = int((y + y + h) / 2)
            center_points_cur_frame.append((cx, cy))
            #print("FRAME N°", count, " ", x, y, w, h)


            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # print(box)

        return box
    #     key = cv2.waitKey(1)
    #     if key == 27:
    #         break
    # cap.release()
    # cv2.destroyAllWindows()


# ///////////////////////////////////////////////////////////////////////////////////

# def add_id():




#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class_names = od.load_class_names("model_class/classes.txt")
allowed_classes = list(class_names)


# print(crop_objects(cap, data, "output/", allowed_classes))
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////