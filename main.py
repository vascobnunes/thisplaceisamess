# This is a program to detect when a given room or desk is a mess.
# The program uses the camera to compare the current status of the room or desk to the reference image.
# This was developed to run on a Raspberry Pi.

# To run this, you need a Raspberry Pi 2 (or greater) with opencv and
# the picamera[array] module installed.

import cv2
import numpy as np
import platform
import time
import imutils
import os

# from skimage.metrics import structural_similarity as ssim

print("Press Ctrl * C to EXIT")


def talk(msg):
    if platform.system() == "Windows":
        import win32com.client as wincl
        speak = wincl.Dispatch("SAPI.SpVoice")
    else:
        os.system("espeak {} -ven+f5 -k5 -s150 --stdout | aplay -D bluealsa".format(msg))


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def detectmovement2():
    cam = cv2.VideoCapture(0)
    width = 640
    height = 480
    cam.set(3, width)
    cam.set(4, height)
    thres = 20  # set difference between pixel values between frames
    trigger = (height * width) / 10  # 10% of pixels
    winName = "Movement Indicator"
    cv2.namedWindow(winName)

    # Read three images first:
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    # t_minus = cv2.cvtColor(cv2.imread("t0.png"), cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    while True:
        c = diffImg(t_minus, t, t_plus)
        cv2.imshow(winName, c)
        # Read next image
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        c[c < thres] = 0
        c[c >= thres] = 200
        total = np.sum(c) / 200
        if total > trigger:
            print(total)

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyWindow(winName)
            break
    print("Goodbye")


def setTidy():
    width = 640
    height = 480
    cam = cv2.VideoCapture(0)
    t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    cv2.imwrite("t0.png", t0)


def main1(tidy):
    blur = 51
    tidy = cv2.imread(tidy)
    tidy_g = cv2.cvtColor(tidy, cv2.COLOR_RGB2GRAY)
    tidy_g = cv2.GaussianBlur(tidy_g, (blur, blur), 0)
    tidy_g = imutils.resize(tidy_g, width=500)
    width = 640
    height = 480
    cam = cv2.VideoCapture(0)
    cam.set(3, width)
    cam.set(4, height)
    t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t0 = cv2.GaussianBlur(t0, (blur, blur), 0)
    t0 = imutils.resize(t0, width=500)
    while True:
        t1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        t1 = cv2.GaussianBlur(t1, (blur, blur), 0)
        t1 = imutils.resize(t1, width=500)
        frameDelta = cv2.absdiff(t1, t0)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow(cv2.namedWindow("tidy"), tidy)
        # cv2.imshow(cv2.namedWindow("current"), cam.read()[1])
        # cv2.imshow(cv2.namedWindow("diff"), thresh)
        if (thresh.sum() > 4):
            print("movement detected")
        else:
            frameDelta_w_tidy = cv2.absdiff(t1, tidy_g)
            thresh_w_tidy = cv2.threshold(frameDelta_w_tidy, 25, 255, cv2.THRESH_BINARY)[1]
            print(thresh_w_tidy.sum())
            if (thresh_w_tidy.sum() > 500):
                print("This place is a mess!")
                talk("This place is a mess!")
                # cv2.imwrite("thresh_w_tidy.png", thresh_w_tidy)
            else:
                print("well done!")
                talk("Well done! Everything seems tidy!")
            cv2.imwrite("thresh_w_tidy.png", thresh_w_tidy)
            time.sleep(10)
        t0 = t1


# setTidy()
tidy = "t0.png"
main1(tidy)
# detectmovement2()
# similarity()
# img1 = "20200821_172235.jpg"
# img2 = "20200821_172249.jpg"
#
# get_match_confidence(img1, img2, mask=None)
