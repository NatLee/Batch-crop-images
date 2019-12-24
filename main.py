import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm

from utils import Options

drawing = True # true if mouse is pressed
startx, starty = -1, -1
endx, endy = -1, -1
roix, roiy = -1, -1
getFlag = False

# mouse callback function
def drawRectangle(event, x, y, flags, param):
    
    global img, roix, roiy, startx, starty, drawing, mode, endx, endy, getFlag

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        startx, starty = x,y
        print('Start: startx= {}, starty= {}'.format(startx, starty))
    elif event == cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:
        if roix == -1:
            img = np.copy(rawImg)
        else:
            img[starty:roiy, startx:roix, 0:1] = rawImg[starty:roiy, startx:roix, 0:1]
        roix, roiy = x, y
        img[starty:y, startx:x, 0:1] = 0  
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        endx, endy = x, y
        print('End: x= {}, y= {}'.format(endx, endy))
        getFlag = True

if __name__ == '__main__':
    
    opt = Options()
    imgs = [img for img in opt.input_path.glob('./*.*[jpg,png,gif]')]
    rawImg = cv2.imread(imgs[0].absolute().as_posix())
    img = rawImg.copy()
    cv2.namedWindow('Crop Window')
    cv2.setMouseCallback('Crop Window', drawRectangle)

    while True:
        cv2.imshow('Crop Window',img)
        if cv2.waitKey(20) and 0xFF == ord('q') or getFlag:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break


    if getFlag:
        for originalImg in tqdm(imgs):
            loadImg = cv2.imread(originalImg.absolute().as_posix())
            cropImg = loadImg[starty +1 :endy + 1, startx + 1:endx + 1, :]
            cv2.imwrite((opt.output_path / originalImg.name).absolute().as_posix(), cropImg)

