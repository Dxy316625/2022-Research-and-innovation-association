# -*- coding: utf-8 -*-
import time
import struct
import cv2 as cv
import numpy as np
import threading
import os
import argparse

from controller import Controller

client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)

global frame

if __name__ == '__main__':
    # creat a controller
    controller = Controller(server_address)
    stop_heartbeat = False
    
    # cap = cv.VideoCapture(4, cv.CAP_V4L2)
    cap = cv.VideoCapture("/dev/video2", cv.CAP_V4L2)
    # cap = cv.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)
    # 图像计数 从1开始
    img_count = 1
    # start to exchange heartbeat pack
    def heart_exchange(con):
        pack = struct.pack('<3i', 0x21040001, 0, 0)
        while True:
            if stop_heartbeat:
                return
            con.send(pack)
            time.sleep(0.25)  # 4Hz
    heart_exchange_thread = threading.Thread(target=heart_exchange, args=(controller,))
    heart_exchange_thread.start()

    # stand up
    print("Wait 10 seconds and stand up......")
    pack = struct.pack('<3i', 0x21010202, 0, 0)
    controller.send(pack)
    time.sleep(5)
    controller.send(pack)
    time.sleep(5)
    controller.send(pack)
    print("Dog should stand up, otherwise press 'ctrl + c' and re-run the demo")
    time.sleep(5)
    
    '''pack = struct.pack('<3i', 0x21010D05, 0, 0)
    controller.send(pack)
    time.sleep(5)
    print('stop ges')
    
    pack = struct.pack('<3i', 0x21010130, -32000, 0)
    controller.send(pack)
    time.sleep(3)
    print('up')'''
    controller.stand_Mode()
    controller.Velocity(-32768, 0, 0)
    #pack = struct.pack('<3i', 0x21010209, 0, 0)
    #controller.send(pack)

    while(1):
        ret, frame = cap.read()
        if ret:
            # show a frame
            cv.imshow("capture", frame)
            # 等待按键事件发生 等待1ms
            key = cv.waitKey(1)
            if key == ord('q'):
                # 如果按键为q 代表quit 退出程序
                print("程序正常退出..")
                break
            elif key == ord('s'):
                ## 如果s键按下，则进行图片保存
                # 写入图片 并命名图片为 图片序号.png
                cv.imwrite("s1/{}.png".format(img_count), frame)
                print("保存图片，名字为  {}.png".format(img_count))
                # 图片编号计数自增1
                img_count += 1
        else:
            print("图像数据获取失败！！")
            break

    pack = struct.pack('<3i', 0x21010202, 0, 0)
    controller.send(pack)
    cap.release()
    cv.destroyAllWindows()
    stop_heartbeat = True

