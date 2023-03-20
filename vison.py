import cv2 as cv2
import numpy as np


class Vision:
    def __init__(self, camera, max_frames, min_dist, p1, p2, min_radius, max_radius, lower, upper):
        self.cap = cv2.VideoCapture(camera)
        if not self.cap.isOpened():
            assert 'FCK U', 'Can\'t open camera!'

        self.lost_frames = 0
        self.max_frames = max_frames

        self.min_dist = min_dist
        self.para1 = p1
        self.para2 = p2
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.lower_color = lower
        self.upper_color = upper

        self.ball_coordinate = []

        self.frame = None

    def __frame(self):
        ret, frame = self.cap.read()
        if not ret:
            assert 'FCK U', 'Can\'t get frame!'
        self.frame = frame
        cv2.waitKey(1)

    def __image_preprocessor(self):
        frame_temp = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        frame_temp = cv2.inRange(self.frame, self.lower_color, self.upper_color)
        frame_temp = cv2.GaussianBlur(self.frame, (5, 5), 0)
        return frame_temp

    def __find_circus(self, frame):
        c = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1, self.min_dist, param1=self.para1, param2=self.para2,
                                minRadius=self.min_radius, maxRadius=self.max_radius)
        max_area = 0
        circle = []
        for i in c[0,:]:
            area = 3.1415 * i[2] * i[2]
            if max_area < area:
                max_area = area
                circle = i
        return circle

    @property
    def size(self):
        self.__frame()
        (h, w, d) = self.frame.shape
        return w, h

    @property
    def get_coordinate(self):
        self.__frame()
        coordinate = self.__find_circus(self.__image_preprocessor())

        if coordinate is not None:
            self.lost_frames = 0
            self.ball_coordinate = coordinate
            return self.ball_coordinate
        elif self.lost_frames < self.max_frames:
            self.lost_frames += 1
            return self.ball_coordinate
        else:
            return None
