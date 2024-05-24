import cv2
import onnxruntime as ort
from PIL import Image
import numpy as np
import time
from controller import Controller
import os
import pygame
import struct
import threading
from model_recognize import init_detect_model
from model_recognize import detect_object
from model_recognize import voice
from model_recognize import voice_id



client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
Develop_Mode = False

if __name__ == '__main__':
    controller = Controller(server_address)
    stop_heartbeat = False

    # 模型文件的路径
    model_path = "best.onnx"
    # 初始化检测模型，加载模型并获取模型输入节点信息和输入图像的宽度、高度
    session, model_inputs, input_width, input_height = init_detect_model(model_path)
    # 打开摄像头

    if Develop_Mode:
        cap = cv2.VideoCapture(0)

        # from Robot Dog
    else:
        cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)



        def heart_exchange(con):
            pack = struct.pack('<3i', 0x21040001, 0, 0)  # json
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

        # print("Waiting 15s......")
        # time.sleep(10)
        # print("Rotating...")
        # controller.send(struct.pack('<3i', 0x21010D05, 0, 0))
        # time.sleep(3)  # need time to turn 360 degrees
        # controller.send(struct.pack('<3i', 0x21010135, -32500, 0))
        # time.sleep(5)
        # print(4)
        # controller.send(pack)
        # stop_heartbeat = True
    # try to use CUDA
    if cv2.cuda.getCudaEnabledDeviceCount() != 0:
        backend = cv2.dnn.DNN_BACKEND_CUDA
        target = cv2.dnn.DNN_TARGET_CUDA
    else:
        backend = cv2.dnn.DNN_BACKEND_DEFAULT
        target = cv2.dnn.DNN_TARGET_CPU
        print('CUDA is not set, will fall back to CPU.')

    # cap = cv2.VideoCapture(0)  # 0表示默认摄像头，如果有多个摄像头可以尝试使用1、2等
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    # 初始化帧数计数器和起始时间
    frame_count = 0
    start_time = time.time()
    # 循环读取摄像头视频流

    global is_speak
    global id_temp
    is_speak = True
    id_temp = None

    recognize_cnt=0

    id_buffer = []
    voice_num = []
    controller.stand_Mode()
    controller.Velocity(-32768, 0, 0)
    while True:
        # 按下 'q' 键退出循环
        k = cv2.waitKey(1)
        if k == 113 or k == 81:  # q or Q to quit
            print("Demo is quiting......")
            if not Develop_Mode:
                controller.drive_dog("squat")
            cap.release()
            cv2.destroyWindow("Demo")
            stop_heartbeat = True
            is_speak = False
            break

        if recognize_cnt<=4:
            # 读取一帧
            if recognize_cnt % 2 == 0:
                ret, frame = cap.read()
                # 检查帧是否成功读取
                if not ret:
                    print("Error: Could not read frame.")
                    break
                # 使用检测模型对读入的帧进行对象检测
                output_image, id, box = detect_object(frame, session, model_inputs, input_width, input_height)
                id_temp = id
                if id is not None:
                    id_buffer.append(id)
                print(id_buffer)
                print(len(id_buffer))
                if len(id_buffer) >= 3:
                    if all(val == id_buffer[0] for val in id_buffer):  # 检查是否连续三次识别结果相同
                        voice_num = voice_id(id_buffer[0])
                        if voice_num[0] is not None and voice_num[1] is not None:
                            voice(voice_num[0])
                            voice(voice_num[1])
                            voice(voice_num[2])
                            id_buffer.clear()
                            recognize_cnt = recognize_cnt + 1
                            if voice_num[2]!=14:
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                controller.Stop()
                                controller.stand_Mode()
                                controller.Velocity(-25000, 0, 0)
                                time.sleep(1)
                                controller.Stop()
                                time.sleep(1)
                                controller.stand_Mode()
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                controller.Stop()
                                controller.stand_Mode()
                                controller.Velocity(-25000, 0, 0)
                                controller.Stop()
                            else:
                                controller.Velocity(0, 25000, 0)
                                time.sleep(1)
                                controller.Stop()
                                controller.stand_Mode()
                                controller.Velocity(0, -25000, 0)
                                time.sleep(1)
                                controller.Stop()
                                controller.stand_Mode()
                                controller.Velocity(0, 25000, 0)
                                time.sleep(1)
                                controller.Stop()
                                controller.stand_Mode()
                                controller.Velocity(0, -25000, 0)
                                controller.Stop()
                            continue
                    else:
                        id_buffer.clear()  # 重置缓冲区
                        id_buffer.append(id)  # 更新上一个识别结果为当前识别结果

                if box != None:
                    x1, y1, w, h = box
                    s = w * h
                    print(s)
                # output_image, id = detect_object('capture_screenshot_79.png', session, model_inputs, input_width, input_height)
                # 计算帧速率
                frame_count += 1
                end_time = time.time()
                elapsed_time = end_time - start_time
                fps = frame_count / elapsed_time

                print(f"FPS: {fps:.2f}")
                # if(id!=None):
                #     pyttsx3.speak(id)
                print(id)
                # print(w,h)
                # 将FPS绘制在图像上
                cv2.putText(output_image, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)
                # 在窗口中显示当前帧
                cv2.imshow("Demo", output_image)

            elif recognize_cnt % 2 == 1:
                controller.Stop()
                controller.Move_Mode()
                time.sleep(2)
                controller.Velocity(7100, -25000, 0)
                time.sleep(8)
                controller.Stop()
                time.sleep(1)
                controller.stand_Mode()
                controller.Velocity(-32768, 0, 0)
                recognize_cnt = recognize_cnt + 1
                for i in range(50):
                    ret, frame = cap.read()

        else:
            controller.Stop()
            controller.Move_Mode()

