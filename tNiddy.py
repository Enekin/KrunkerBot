import threading
import time
import cv2

from pynput.mouse import Controller
from gfxHandler import GfxHandler
from loguru import logger


class Position:
    def __init__(self):
        self.pos = (0, 0)

    def set(self, tpos):
        self.pos = tpos

    def get(self):
        return self.pos


class Target:
    def __init__(self):
        self.current = Position()
        self.prev = Position()


logger.info("Initializing gfx handler..")
cap = GfxHandler(1100, 500, 620, 415)
target = Target()
img = cap.get_frame()
stop = False


def gfx():
    global img
    global stop
    target_low = (88, 85, 220)
    target_high = (93, 95, 250)
    template = cv2.imread("maskedhp.png", 1)
    while True:
        if stop:
            break
        img = cap.get_frame()
        img = cv2.circle(img, (int(cap.width / 2), int(cap.height / 2)), 4, (255, 255, 255))
        mask = cv2.inRange(img, target_low, target_high)
        imgC = cv2.bitwise_and(img, img, mask=mask)
        hit = cap.find_template(imgC, template)
        if hit != (0, 0):
            img = cv2.circle(img, ((hit[0] + 31), (hit[1] + 20)), 5, (0, 0, 255))
        target.prev.set(target.current.get())
        target.current.set((hit[0], hit[1]))
        time.sleep(0.05)


def aim():
    global cap
    global target
    global stop
    mouse = Controller()
    while True:
        if stop:
            break
        cur = target.current.get()
        if cur == (0, 0):
            continue
        pre = target.prev.get()
        # rheadpos = (int(cur[0]+(cur[0]-pre[0]) - cap.width/2)+31, int(cur[1]+(cur[1]-pre[1]) - cap.height/2)+15)
        rheadpos = (int(cur[0] - cap.width/2)+31, int(cur[1] - cap.height/2)+20)
        logger.debug("moving mouse to " + str(rheadpos))
        mouse.move(rheadpos[0]*1.6, rheadpos[1]*1.3)
        target.current.set((0, 0))
        target.prev.set((0, 0))
        time.sleep(0.05)


def main():
    global cap
    global stop
    global target
    # targetcolor = (91, 90, 235)
    logger.info("Bot started")
    imgt = threading.Thread(target=gfx)
    imgt.start()
    aimt = threading.Thread(target=aim)
    aimt.start()
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # temp_w, temp_h = template.shape
    while True:
        key = cv2.waitKey(10)
        if key == 13:
            stop = True
            break

        '''
        prev_rheadpos = (0,0)
        for hit in hits:
            #img = cv2.rectangle(img, (hit[0]+1, hit[1]+1), (hit[0]+temp_h-2, hit[1]+temp_w-2), (0, 255, 0))
            img = cv2.circle(img, ((hit[0] + 30), (hit[1] + 10)), 5, (0,0,255))

            rheadpos = (int((hit[0]+30) - cap.width/2), int((hit[1]+20) - cap.height/2))
            mouse.move(int(rheadpos[0] + prev_rheadpos[0]*0.6), int(rheadpos[1]*1.2 - prev_rheadpos[1]*0.2))
            prev_rheadpos = (int(rheadpos[0]*1.1), int(rheadpos[1]*1.1))
            break
        ''' # Multiple targets
        cv2.imshow("tNiddy", img)

    logger.info("Disconnecting..")
    cv2.destroyAllWindows()
    exit(0)


if __name__ == '__main__':
    main()
