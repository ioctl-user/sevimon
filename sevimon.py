#!/usr/bin/python3

# Licensed under AGPLv3+

import os
import sys

os.environ["OPENCV_LOG_LEVEL"]="FATAL" # Suppress OpenCV messages

import cv2
import numpy
from datetime import datetime
import platformdirs
from hsemotion_onnx.facial_emotions import HSEmotionRecognizer

sys.path.append(os.path.dirname(__file__))
from lib.centerface import CenterFace
from lib.i18n import _
from lib.config import *
from lib.cam import *


def writestat(cfg, i, scores) -> None:
    now = datetime.now()
    print(f'{now.strftime("%H:%M:%S")} ', end='')

    # Print scores
    emax = numpy.argmax(scores)
    print(f'[{i}]: {emotions[emax]}; ', end='')
    for e in range(len(emotions)):
        print(f'{emotions[e]}: {scores[e]:4.1f}', end='')
        if e < (len(emotions) - 1):
            print(f', ', end='')
        else:
            print('')

    # Write to logs
    if cfg.writestat:
        if not os.path.exists(platformdirs.user_log_dir(ANAME)):
            os.makedirs(platformdirs.user_log_dir(ANAME))
        fp = open(platformdirs.user_log_dir(ANAME) + "/" + now.strftime("%Y.%m.%d"), 'a')
        str = now.strftime("%H:%M:%S")
        for e in range(len(emotions)):
            str = str + " %4.1lf" % (scores[e])
        str = str + "\n"
        fp.write(str)
        fp.close()


def warn_actions(cfg, i, scores, wws):
    # Check warning state and notify user
    wname = "Face warn"
    ws = False # Warning state flag
    for e in range(len(emotions)):
        if cfg.wmin[e] is not None and scores[e] < cfg.wmin[e]:
            ws = True
            break
        if cfg.wmax[e] is not None and scores[e] > cfg.wmax[e]:
            ws = True
            break
    try:
        # Show warning window in case of:
        #     it's warning condition, it's on in cfg, has no warning window yet
        if ws and cfg.showwarn and not wws:
            # Use OpenCV to avoid excess dependencies

            w = cfg.wsize
            h = cfg.wsize
            if sys.platform == 'darwin' and w < 200:
                # Mac OS doesn't allow windows width less than 200, so...
                w = 200

            wimg = numpy.zeros((h, w, 3), numpy.uint8)
            wimg = cv2.rectangle(wimg, (0, 0), (w - 1, h - 1), cfg.wcolor, -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "!"
            linew = int(h / 32)
            textsize = cv2.getTextSize(text, font, 1, linew)[0]
            textx = int((wimg.shape[1] - textsize[0]) / 2)
            texty = int((wimg.shape[0] + textsize[1]) / 2)
            cv2.putText(wimg, "!", (textx, texty), font, 1, (0, 0, 0), linew)
            cv2.namedWindow(wname, cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO | cv2.WINDOW_GUI_NORMAL)
            cv2.resizeWindow(wname, w, h)
            cv2.moveWindow(wname, cfg.wx, cfg.wy)
            cv2.setWindowProperty(wname, cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow(wname, wimg)
        # Destroy warning window in case of:
        #     it's not to be shown (cfg and condition) and has previous window
        elif not (cfg.showwarn and ws) and wws:
            cv2.destroyWindow(wname)

        if ws and cfg.beepwarn:
            # Generate system beep
            print("\a", end="")
    except Exception as exc:
        print(f'Warning: {exc}')

    return ws and cfg.showwarn


def main() -> None:
    MODEL_NAME='enet_b0_8_best_vgaf'
    cfg = readcfg()
    cam = cam_class(cfg)
    wws = False # Warning windows was shown flag

    ret, cap = cam.find_camera()
    if ret is False:
        return -1

    # Set main window properties
    cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)

    # Set neural networks
    centerface = CenterFace()
    fer = HSEmotionRecognizer(MODEL_NAME)

    while True:
        ret, image_bgr = cam.get_next_frame()
        if not ret:
            print(_("Can't read camera image"))
            return -1

        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        bounding_boxes, ign = centerface(image_bgr, image_bgr.shape[0], image_bgr.shape[1], threshold=0.35)

        i = 0
        for bbox in bounding_boxes:
            x1, y1, x2, y2 = [round(b) for b in bbox[0:4]]
            if (x1 <= 0): x1 = 0
            if (y1 <= 0): y1 = 0
            if (x2 >= image_bgr.shape[1]): x2 = image_bgr.shape[1] - 1
            if (y2 >= image_bgr.shape[0]): y2 = image_bgr.shape[0] - 1

            face_img = image[y1:y2, x1:x2]
            emotion, scores = fer.predict_emotions(face_img,logits=True)
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (255, 0, 0), 1)

            wws = warn_actions(cfg, i, scores, wws)
            writestat(cfg, i, scores)

            i = i + 1

        if cfg.showcap:
            # Exit if main window was closed by user
            if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
                break

            # Show captured image with the detected box
            cv2.imshow('Video', image_bgr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    main()

# vi: tabstop=4 shiftwidth=4 expandtab
