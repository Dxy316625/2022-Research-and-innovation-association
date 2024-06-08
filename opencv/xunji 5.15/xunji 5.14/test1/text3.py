import time
import struct
import cv2
import os
import pygame
from controller import Controller
from qcode_detect import decodeDisplay
from RoadSignRecognition import RoadSignRecognition
import threading
from line import line

from model_recognize import init_detect_model
from model_recognize import detect_object
from model_recognize import voice
from model_recognize import voice_id

client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
Develop_Mode = False

global contest_process
global stop_heartbeat
global sign
global qcode_content
global is_capture
global line_find_flag
global is_line
global is_line_flag
global is_capture_flag
global is_running
global is_running_flag
global run_cnt
is_line = True
is_line_flag = False
is_capture_flag = False
contest_process = 0
qcode_content = None
sign = None
is_capture = True

is_running = True
is_running_flag = True
run_cnt = 0

recognize_cnt = 0

id_buffer = []
voice_num = []


def voice_turn(item):
    turn = None
    if item == "turn left":
        turn = 5
    if item == "turn right":
        turn = 6
    return turn


def voice_qcode(item):
    qcode = None
    if item == "A":
        qcode = 16
    if item == "B":
        qcode = 19
    if item == "C":
        qcode = 0
    return qcode


if __name__ == '__main__':
    sign_detector = RoadSignRecognition()
    controller = Controller(server_address)
    stop_heartbeat = False

    model_path = "best.onnx"
    session, model_inputs, input_width, input_height = init_detect_model(model_path)

    if Develop_Mode:
        cap = cv2.VideoCapture(0)
        # cap1 = cv2.VideoCapture(1)
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

        print("Wait 10 seconds and stand up......")
        pack = struct.pack('<3i', 0x21010202, 0, 0)
        controller.send(pack)
        time.sleep(5)
        controller.send(pack)
        time.sleep(5)
        controller.send(pack)
        print("Dog should stand up, otherwise press 'ctrl + c' and re-run the demo")

    if cv2.cuda.getCudaEnabledDeviceCount() != 0:
        backend = cv2.dnn.DNN_BACKEND_CUDA
        target = cv2.dnn.DNN_TARGET_CUDA
    else:
        backend = cv2.dnn.DNN_BACKEND_DEFAULT
        target = cv2.dnn.DNN_TARGET_CPU
        print('CUDA is not set, will fall back to CPU.')

    global results
    global img

    line_find_flag = False


    def run_control():
        global is_running
        global contest_process
        global sign
        global is_running_flag
        cnt = 0
        qianjin = 0
        zuoyou = 0
        while is_running:
            while is_running_flag:
                if contest_process == 0:
                    controller.Velocity(7000, 25000, 0)
                    time.sleep(10)
                    controller.Velocity(0, 0, 0)
                    time.sleep(1)
                    controller.stairs_Mode()
                    controller.Velocity(8000, 0, 0)
                    time.sleep(9)
                    controller.Walk_Mode()
                    controller.Stop()
                    contest_process = contest_process + 1
                    is_running_flag = False
                elif contest_process == 1:
                    # controller.Velocity(8000, 0, 0)
                    # time.sleep(1)
                    # controller.Velocity(-8000, 0, 0)
                    # time.sleep(1)
                    controller.Velocity(-8000, 0, 0)
                    time.sleep(1)
                    controller.Stop()

                elif contest_process == 3:
                    print(sign)
                    if sign == "turn left":
                        print(cnt)

                        ret, frame = cap.read()
                        if ret is None or not ret:
                            continue
                        height, width = frame.shape[:2]

                        line1 = line(width, height)
                        results, img = line1.check_line(frame)
                        print(results)

                        if cnt == 0:
                            controller.Walk_Mode()
                            controller.Velocity(7000, 0, 0)
                            time.sleep(1.5)
                            controller.Turn(1)
                            time.sleep(1)
                            controller.Stop()
                            cnt = 1
                        elif cnt == 8:
                            controller.Velocity(8600, 0, 0)
                            time.sleep(5)
                            controller.Stop()
                            is_running_flag = False
                            controller.stand_Mode()
                            controller.Velocity(-32768, 0, 0)
                            time.sleep(1)
                            contest_process = 4
                            continue
                        if (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 8800
                            zuoyou = 0
                        elif (results[0] == 0 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 7800
                            zuoyou = 17000  # 17000~20000(左为正，右为负)
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 7300
                            zuoyou = 18500  # 17000~20000(左为正，右为负)
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[
                            4] == 0):
                            qianjin = 7800
                            zuoyou = -17000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[
                            4] == 1):
                            qianjin = 7300
                            zuoyou = -18500
                        elif (results[0] == 1 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 7000
                            zuoyou = 20000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[
                            4] == 1):
                            qianjin = 7000
                            zuoyou = -20000
                        elif (results[0] == 1 and results[1] == 1 and results[3] == 0 and results[4] == 0):
                            controller.Walk_Mode()
                            if cnt == 6:
                                controller.Velocity(8000, 0, 0)
                                time.sleep(2.5)
                                controller.Turn(1)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                cnt = 7
                            elif cnt == 5:
                                controller.Stop()
                                time.sleep(1)
                                controller.stairs_Mode()
                                controller.Velocity(9000, 0, 0)
                                time.sleep(4)
                                cnt = 6
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[
                            4] == 1):
                            controller.Velocity(8500, 0, 0)
                            time.sleep(3)
                            controller.Velocity(0, 0, 0)
                            time.sleep(1)
                            controller.Turn(1)
                            time.sleep(1)
                            controller.Velocity(7000, 0, 0)
                            if cnt == 4:
                                cnt = 5
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[
                            4] == 0):
                            print(cnt)
                            if cnt == 2:
                                print("hhh")
                                controller.Velocity(9000, 0, 0)
                                time.sleep(2.5)
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                cnt = 3
                            elif cnt == 3:
                                controller.Walk_Mode()
                                controller.Velocity(7000, -25000, 0)
                                time.sleep(9)
                                controller.Velocity(8000, 0, 0)
                                cnt = 4
                            # elif cnt == 8:
                            #     time.sleep(2)
                            #     controller.Stop()
                            #     contest_process = 4
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 1 and results[
                            4] == 1):
                            print(1)
                            if cnt == 1:
                                controller.Velocity(8500, 10000, 0)
                                time.sleep(2.5)
                                controller.Turn(0)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                controller.stairs_Mode()
                                time.sleep(1)
                                cnt = 2
                            elif cnt == 7:
                                controller.Velocity(8500, 0, 0)
                                time.sleep(3)
                                controller.Turn(0)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                cnt = 8
                        controller.Velocity(int(qianjin), int(zuoyou), 0)


                    elif sign == "turn right":
                        print(cnt)

                        ret, frame = cap.read()
                        if ret is None or not ret:
                            continue
                        height, width = frame.shape[:2]

                        line1 = line(width, height)
                        results, img = line1.check_line(frame)
                        print(results)

                        if cnt == 0:
                            controller.Walk_Mode()
                            controller.Velocity(8000, 0, 0)
                            time.sleep(2)
                            controller.Turn(0)
                            time.sleep(1)
                            controller.Stop()
                            cnt = 1

                        elif cnt == 6:
                            controller.Velocity(8600, 0, 0)
                            time.sleep(5)
                            controller.Stop()
                            is_running_flag = False
                            controller.stand_Mode()
                            controller.Velocity(-32768, 0, 0)
                            time.sleep(1)
                            contest_process = 4
                            continue

                        if (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 8500
                            zuoyou = 0
                        elif (results[0] == 0 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 7500
                            zuoyou = 17000  # 17000~20000(左为正，右为负)
                        # elif (results[0] == 1 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                        #    qianjin =7000
                        #   zuoyou = 18500     #17000~20000(左为正，右为负)
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[
                            4] == 0):
                            qianjin = 7500
                            zuoyou = -17000
                        # elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[4] == 1):
                        #   qianjin = 7000
                        #  zuoyou = -18500
                        elif (results[0] == 1 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[
                            4] == 0):
                            qianjin = 7000
                            zuoyou = 20000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[
                            4] == 1):
                            qianjin = 7000
                            zuoyou = -20000
                        elif (results[0] == 1 and results[1] == 1 and results[3] == 0 and results[
                            4] == 0):
                            if cnt == 1:
                                controller.Walk_Mode()
                                controller.Velocity(8500, 0, 0)
                                time.sleep(3)
                                controller.Turn(1)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                controller.stairs_Mode()
                                time.sleep(1)
                                cnt = 2
                            elif cnt == 3:
                                controller.Stop()
                                controller.stairs_Mode()
                                controller.Velocity(9000, 0, 0)
                                time.sleep(4)
                                cnt = 4
                            elif cnt == 4:
                                controller.Walk_Mode()
                                controller.Velocity(8500, 0, 0)
                                time.sleep(3.3)
                                controller.Turn(1)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                cnt = 5
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[
                            4] == 1):
                            time.sleep(1.3)
                            controller.Velocity(0, 0, 0)
                            controller.Walk_Mode()
                            time.sleep(1)
                            controller.Velocity(8300, 0, 0)
                            time.sleep(2)
                            controller.Turn(1)
                            time.sleep(1)
                            controller.Velocity(7000, 0, 0)
                            
                            if cnt == 2:
                                
                                cnt = 3

                        elif (results[0] == 0 and results[1] == 0 and results[3] == 1 and results[4] == 1):
                            if cnt == 5:
                                controller.Velocity(8500, 0, 0)
                                time.sleep(3)
                                controller.Walk_Mode()
                                time.sleep(1)
                                controller.Turn(0)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                cnt = 6
                        controller.Velocity(int(qianjin), int(zuoyou), 0)

                if stop_heartbeat:
                    break
            if stop_heartbeat:
                break


    run_control_thread = threading.Thread(target=run_control, args=())
    run_control_thread.start()
    controller.Move_Mode()
    sign1 = 0
    qcode1 = 0

    while True:
        if (stop_heartbeat):
            is_capture = False
            is_line = False
            break
        # print(contest_process)

        if (contest_process == 1):
            # contest2_flag = True
            ret, frame = cap.read()
            if ret is None or not ret:
                continue
            height, width = frame.shape[:2]

            line1 = line(width, height)
            results, img = line1.check_line(frame)
            cv2.imshow('Demo', img)

            print(results)
            if (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1):
                print("find_line")
                results=None
                contest_process = contest_process + 1
                is_running_flag = False
                # time.sleep(2)
                controller.Velocity(0, 0, 0)
                time.sleep(1)
                controller.Velocity(8000, 0, 0)
                time.sleep(3.5)
                controller.Stop()
                controller.stand_Mode()
                controller.Velocity(-32768, 0, 0)
                continue
            else:
                is_running_flag = True



        elif (contest_process == 2):

            contest3_flag = True
            ret, frame = cap.read()
            if ret is None or not ret:
                continue

            bbox = sign_detector.detect(frame)
            frame = sign_detector.visualize(frame)
            sign = sign_detector.classify(frame)

            cv2.imshow("Demo", frame)
            image = frame.copy()

            if qcode_content == None:
                qcode_content = decodeDisplay(image)
            qcode_content = 'A'
            sign='turn right'
            print(qcode_content)
            if qcode_content is not None and sign is not None:
                print("标志:{} ".format(sign))
                print("二维码:{} ".format(qcode_content))
                sign1 = voice_turn(sign)
                qcode1 = voice_qcode(qcode_content)
                voice(sign1)
                voice(qcode1)

                # is_capture_flag = False
                controller.Move_Mode()
                controller.Walk_Mode()
                contest_process = contest_process + 1




        elif (contest_process == 3):
            if contest3_flag == True:
                is_running_flag = True
                contest3_flag = False

            ret, frame = cap.read()
            if ret is None or not ret:
                continue
            height, width = frame.shape[:2]

            line1 = line(width, height)
            results, img = line1.check_line(frame)
            cv2.imshow('Demo', img)


        elif (contest_process == 4):
            if recognize_cnt <= 4:
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
                            if voice_num[0] is not None and voice_num[1] is not None and voice_num[2] is not None:
                                voice(voice_num[0])
                                voice(voice_num[1])
                                voice(voice_num[2])
                                id_buffer.clear()
                                recognize_cnt = recognize_cnt + 1
                                if voice_num[2] != 14:
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

                    print(id)

                    cv2.imshow("Demo", output_image)

                elif recognize_cnt % 2 == 1:
                    controller.Stop()
                    controller.Move_Mode()
                    time.sleep(2)
                    controller.Velocity(6900, 25000, 0)
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
                controller.Velocity(6900, -25000, 0)
                time.sleep(3)
                controller.Stop()
                controller.Walk_Mode()
                cnt = 0
                contest_process = 5


        elif contest_process == 5:
            controller.Velocity(8500, 0, 0)
            time.sleep(3)
            controller.Stop()
            time.sleep(3)
            controller.Turn(0)
            time.sleep(1.3)
            controller.Stop()
            time.sleep(2)
            controller.Velocity(9000, 14000, 0)
            while True:
                ret, frame = cap.read()
                if ret is None or not ret:
                    continue
                results, img = line1.check_line(frame)
                print(results)
                if cnt == 0:
                    if (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[
                        4] == 1):
                        controller.Stop()
                        cnt = 1
                elif cnt == 1:
                    if (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[
                        4] == 1):
                        controller.Velocity(7000, -25000, 0)
                    elif (results[0] == 1 and results[1] == 1 and results[3] == 0 and results[4] == 0):
                        controller.Stop()
                        cnt = 2
                elif cnt == 2:
                    if (qcode_content=='C'):
                        controller.Velocity(7000, 25000, 0)
                        time.sleep(3)  # 位移距离
                        controller.Stop()
                        controller.stairs_Mode()
                        time.sleep(1)
                        controller.Velocity(9000, 0, 0)
                        time.sleep(4)
                        controller.Stop()
                        break
                    elif (qcode_content=='B'):
                        controller.Velocity(7000, 25000, 0)
                        time.sleep(9)  # 位移距离
                        controller.Stop()
                        controller.stairs_Mode()
                        time.sleep(1)
                        controller.Velocity(9000, 0, 0)
                        time.sleep(4)
                        controller.Stop()
                        break
                    elif (qcode_content=='A'):
                        controller.Velocity(7000, 25000, 0)
                        time.sleep(15)  # 位移距离
                        controller.Stop()
                        controller.stairs_Mode()
                        time.sleep(1)
                        controller.Velocity(9000, 0, 0)
                        time.sleep(4)
                        controller.Stop()
                        break
            controller.Stop()
            time.sleep(5)
            controller.send(struct.pack('<3i', 0x21010202, 0, 0))

        k = cv2.waitKey(1)
        if k == 113 or k == 81:  # q or Q to quit
            print("Demo is quiting......")
            if not Develop_Mode:
                controller.drive_dog("squat")
            cap.release()
            cv2.destroyWindow("Demo")
            stop_heartbeat = True
            # is_line = False
            is_running = False
            break
