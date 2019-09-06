from loguru import logger
from PIL import ImageGrab
import numpy as np
import pyautogui
import cv2


class GfxHandler:
    def __init__(self, fX, fY, width, height):
        """Setting bBox (zone that pNiddy is running in)"""
        self.threshold = 0.95
        self.res_width, self.res_height = pyautogui.size()
        try:
            self.fX = int(fX)
            self.fY = int(fY)
            self.width = int(width)
            self.height = int(height)
            self.tX = self.fX + int(width)
            self.tY = self.fY + int(height)
        except Exception as e: # if other datatypes than ints were sent
            logger.error("Wrong datatypes passed, accepting INTs only!")
            exit(1)

    def get_frame(self):
        """Returns frame from bBox"""
        # noinspection SpellCheckingInspection
        img = ImageGrab.grab(bbox=(self.fX, self.fY, self.tX, self.tY))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB) # convert to grayscale
        # cv2.imshow("test", frame)
        return frame

    def find_templates(self, img, template):
        """find multiple templates in img"""
        img_gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gs, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        zippedObjs = zip(*loc[::-1])
        return zippedObjs

    def find_template(self, img, template):
        """find single template in img"""
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        if top_left != (0, 0):
            return top_left
        return (0, 0)


if __name__ == '__main__':
    logger.error("This is a module and not meant to be run as main")
    exit(0)
