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


class Talker:
    def __init__(self, msg):
        self.msg = msg

    def talk(self):
        if platform.system() == "Windows":
            import win32com.client as wincl
            speak = wincl.Dispatch("SAPI.SpVoice")
        else:
            os.system("espeak {} -ven+f5 -k5 -s150 --stdout | aplay -D bluealsa".format(self.msg))


class Detector:
    def __init__(self, blur, camera, height, tidy, threshold, width):
        self.blur = blur
        self.camera = camera
        self.height = height
        self.threshold = threshold
        self.width = width
        self.tidy = cv2.imread(tidy)
        self.newtidyoutput = "t0.png"
        self.messmsg = "This place is a mess!"
        self.welldonemsg = "Well done! Everything seems tidy!"

        # self.talk1 = Talker(self.messmsg)
        # t2 = Talker(self.welldonemsg)


    def detectmovement(self):
        pass

    def setarea(self):
        pass

    def settidy(self):
        cam = cv2.VideoCapture(0)
        t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        cv2.imwrite(self.newtidyoutput, t0)
        return self.newtidyoutput

    def main(self):
        print("Press Ctrl * C to EXIT")
        tidy_g = cv2.cvtColor(self.tidy, cv2.COLOR_RGB2GRAY)
        tidy_g = cv2.GaussianBlur(tidy_g, (self.blur, self.blur), 0)
        tidy_g = imutils.resize(tidy_g, width=500)
        cam = cv2.VideoCapture(self.camera)
        cam.set(3, self.width)
        cam.set(4, self.height)
        t0 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        t0 = cv2.GaussianBlur(t0, (self.blur, self.blur), 0)
        t0 = imutils.resize(t0, width=500)
        while True:
            t1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
            t1 = cv2.GaussianBlur(t1, (self.blur, self.blur), 0)
            t1 = imutils.resize(t1, width=500)
            frameDelta = cv2.absdiff(t1, t0)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            # cv2.imshow(cv2.namedWindow("tidy"), tidy)
            # cv2.imshow(cv2.namedWindow("current"), cam.read()[1])
            # cv2.imshow(cv2.namedWindow("diff"), thresh)
            if (thresh.sum() > self.threshold):
                print("movement detected")
            else:
                frameDelta_w_tidy = cv2.absdiff(t1, tidy_g)
                thresh_w_tidy = cv2.threshold(frameDelta_w_tidy, 25, 255, cv2.THRESH_BINARY)[1]
                print(thresh_w_tidy.sum())
                if (thresh_w_tidy.sum() > 500):
                    print("This place is a mess!")
                    Talker.talk(Talker(self.messmsg))
                    # cv2.imwrite("thresh_w_tidy.png", thresh_w_tidy)
                else:
                    print("well done!")
                    Talker.talk(Talker(self.welldonemsg))
                cv2.imwrite("thresh_w_tidy.png", thresh_w_tidy)
                time.sleep(10)
            t0 = t1


# settidy()
d1 = Detector(51, 0, 480, "t0.png", 4, 640)
d1.main()

# detectmovement2()
# similarity()
# img1 = "20200821_172235.jpg"
# img2 = "20200821_172249.jpg"
#
# get_match_confidence(img1, img2, mask=None)
