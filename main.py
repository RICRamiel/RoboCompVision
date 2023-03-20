import cmSerial
import vison
import numpy as np
import time

if __name__ == '__main__':
    vs = vison.Vision(0, 20, 10, 20, 23, 200, 500,
                      np.array([0, 125, 33], dtype="uint8"), np.array([9, 255, 255], dtype="uint8"))
    ser = cmSerial.cmSerial("/dev/ttyUSB0", 57600)
    w, h = vs.size

    frame_time = int(time.asctime(time.gmtime(0)) * 1000)

    fps = 30
    fps = int(1000 / fps)

    while True:
        if int(time.asctime(time.gmtime(0)) * 1000) - frame_time > fps:
            frame_time = int(time.asctime(time.gmtime(0)) * 1000)
            xc, yc, rc = vs.get_coordinate

            if xc > 420:
                if yc < 120:
                    ser.send_data(2048)
                    print("Пинаю правой ногой")
                else:
                    ser.send_data(512)
                    print("Иду к вперёд (мяч по правой ноге)")

            if xc < 420 and xc > 210:
                ser.send_data(768)
                print("Смещаюсь вправо")

            if xc < 210:
                if yc < 120:
                    ser.send_data(1024)
                    print("Пинаю левой ногой")
                else:
                    ser.send_data(512)
                    print("Иду к вперёд (мяч по левой ноге)")
