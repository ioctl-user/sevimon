#!/usr/bin/python3

# Licensed under AGPLv3

import os
import cv2
import numpy
from datetime import datetime
import platformdirs

from lib.centerface import CenterFace


from hsemotion.facial_emotions import HSEmotionRecognizer

# from cfg import *
from lib.i18n import emotions
from lib.config import *


MODEL_NAME='enet_b0_8_best_afew'


def writestat(i, scores) -> None:
    appname = "sevimon"
    now = datetime.now()
    print(now.strftime("%H:%M:%S "), end='')

    # Print scores
    emax = numpy.argmax(scores)
    print("[", i, "]:", emotions[emax], "; ", end='')
    for e in range(len(emotions)):
        print("%s: %4.1lf" % (emotions[e], scores[e]), end='')
        if e < (len(emotions) - 1):
            print(", ", end='')
        else:
            print(" ")

    # Write to logs
    if WRITESTAT:
        if not os.path.exists(platformdirs.user_log_dir(appname)):
            os.makedirs(platformdirs.user_log_dir(appname))
        fp = open(platformdirs.user_log_dir(appname) + "/" + now.strftime("%Y.%m.%d"), 'a')
        str = now.strftime("%H:%M:%S")
        for e in range(len(emotions)):
            str = str + " %4.1lf" % (scores[e])
        str = str + "\n"
        fp.write(str)
        fp.close()


def showwarn(i, scores) -> None:
    # Show window with detected face
    wname = "Face warn"
    ws = False
    for e in range(len(emotions)):
        if WMIN[e] and scores[e] < WMIN[e]:
            ws = True
            break
        if WMAX[e] and scores[e] > WMAX[e]:
            ws = True
            break
    try:
        if ws:
            if cv2.getWindowProperty(wname, cv2.WND_PROP_VISIBLE) < 1:
                # Use OpenCV to avoid excess dependencies
                wimg = numpy.zeros((WSIZE, WSIZE, 3), numpy.uint8)
                wimg = cv2.rectangle(wimg, (0, 0), (WSIZE - 1, WSIZE - 1), WCOLOR, -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = "!"
                linew = int(WSIZE/32)
                textsize = cv2.getTextSize(text, font, 1, linew)[0]
                textx = int((wimg.shape[1] - textsize[0]) / 2)
                texty = int((wimg.shape[0] + textsize[1]) / 2)
                cv2.putText(wimg, "!", (textx, texty), font, 1, (0, 0, 0), linew)
                cv2.namedWindow(wname, cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO | cv2.WINDOW_GUI_NORMAL)
                cv2.resizeWindow(wname, WSIZE, WSIZE)
                cv2.moveWindow(wname, WX, WY) 
                cv2.imshow(wname, wimg)
        else:
            if cv2.getWindowProperty(wname, cv2.WND_PROP_VISIBLE) > 0:
                cv2.destroyWindow(wname)
    except:
        pass


def main() -> None:
    cap = cv2.VideoCapture(CAMERA_DEV)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_H)
    cap.set(cv2.CAP_PROP_FPS, FPS * 2)  # FPS, multiplication by 2 because of hack to clean buffer
    real_fps = int(cap.get(5))  # Get really set FPS
    skip_frames = real_fps / FPS - 1  # Is there a better way?

    centerface = CenterFace()
    fer = HSEmotionRecognizer(model_name=MODEL_NAME)

    while True:
        for i in range(int(skip_frames)):
            cap.grab()
        ret, image_bgr = cap.read()
        if not ret:
            print("Cannot read camera image")
            return

        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
#        dt1 = datetime.now()
        bounding_boxes, points = centerface(image_bgr, IMG_H, IMG_W, threshold=0.35)
#        dt2 = datetime.now()

# XXX 4
        bounding_boxes, _ = centerface(image_bgr, IMG_H, IMG_W, threshold=0.35)

        i = 0
        for bbox in bounding_boxes:
            x1, y1, x2, y2 = [int(_) for _ in bbox[:4]]
            if (x1 < 0): x1 = 0
            if (y1 < 0): y1 = 0
            if (x2 >= IMG_W): x2 = IMG_W - 1
            if (y2 >= IMG_H): y2 = IMG_H - 1

            face_img = image[y1:y2, x1:x2, :]
            emotion, scores = fer.predict_emotions(face_img,logits=True)
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (255, 0, 0), 1)

            if SHOWWARN:
                showwarn(i, scores)
            writestat(i, scores)

            i = i + 1

        if SHOWCAP:
            # HSE image box
            cv2.imshow('Video', image_bgr)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    main()
