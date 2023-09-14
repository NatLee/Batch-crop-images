from tkinter import Tk
import numpy as np
import cv2

class Cropper:

    def __init__(self, img) -> None:

        self.img = img
        self.screen_width, self.screen_height = self.get_screen_info()

        height, width, _ = self.img.shape
        width_scale = width / self.screen_width
        height_scale = height / self.screen_height

        # check if image is too large, we need to resize it
        if width_scale > 1 or height_scale > 1:
            self.ratio = 1 / max(width_scale, height_scale)
            self.img = cv2.resize(self.img, None, fx=self.ratio, fy=self.ratio)
        else:
            self.ratio = 1.0

        self.canvas_img = np.copy(self.img)

        self.start = (-1, -1)
        self.end = (-1, -1)
        self.roi = (-1, -1)

        self.cropped = False

        print('[Processing]')
        print('----------------------------------------')

        self.get_range_for_cropping()

    def get_start_end(self):
        startx, starty = self.start
        endx, endy = self.end
        return (int(startx // self.ratio), int(starty // self.ratio)), (int(endx // self.ratio), int(endy // self.ratio))

    def get_screen_info(self) -> tuple:
        window = Tk()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.destroy()
        return screen_width, screen_height

    # mouse callback function
    def draw_rectangle_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.start = (x, y)
            print(f'Start (x, y) = {self.start}')

        elif event == cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:

            roix, roiy = self.roi
            startx, starty = self.start

            if roix == -1:
                self.canvas_img = np.copy(self.img)

            else:
                # just change B G channel 0:1
                self.canvas_img[starty:roiy, startx:roix, 0:1] = self.img[starty:roiy, startx:roix, 0:1]

            self.roi = (x, y)

            self.canvas_img[starty:y, startx:x, 0:1] = 0

        elif event == cv2.EVENT_LBUTTONUP:

            self.end = (x, y)
            print(f'End (x, y) = {self.end}')
            self.cropped = True
            print('----------------------------------------')

    def get_range_for_cropping(self):

        cv2.namedWindow('Crop Window')
        cv2.setMouseCallback('Crop Window', self.draw_rectangle_callback)

        while True:
            cv2.imshow('Crop Window', self.canvas_img)
            if cv2.waitKey(20) and 0xFF == ord('q') or self.cropped:
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                break
        return