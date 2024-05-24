import time
import struct
import cv2
import numpy as np
from controller import Controller
from qcode_detect import decodeDisplay
from RoadSignRecognition import RoadSignRecognition
import threading
from line import line

client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
Develop_Mode = True

# Controller = Controller(server_address)
#
#
# cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
# def heart_exchange(con):
#     pack = struct.pack('<3i', 0x21040001, 0, 0)
#     while True:
#         con.send(pack)
#         time.sleep(0.25)  # 4Hz
#
# heart_exchange_thread = threading.Thread(target = heart_exchange, args = (Controller, ))
# heart_exchange_thread.start() # 心跳
global contest_process
contest_process=0
global stop_heartbeat
global sign
sign =None

if __name__ == '__main__':
    sign_detector = RoadSignRecognition()
    controller = Controller(server_address)
    stop_heartbeat = False

    if Develop_Mode:
        cap = cv2.VideoCapture(0)
        cap1 = cv2.VideoCapture(1)
    # from Robot Dog
    else:
        cap = cv2.VideoCapture("/dev/video4", cv2.CAP_V4L2)
        cap1 = cv2.VideoCapture("/dev/video6", cv2.CAP_V4L2)
        #engine = pyttsx3.init()
        #engine.setProperty('voice', 'zh')
        # cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        # cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        def heart_exchange(con):
            pack = struct.pack('<3i', 0x21040001, 0, 0)  #json
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


    global width
    global height
    global is_line
    global results
    global img
    global line_find_flag


    line_find_flag=False
    width=640
    height=800
    def line_recognize():
        global line_find_flag
        global results
        global img
        global stop_heartbeat
        global is_line
        is_line = True
        while is_line:
            ret, frame = cap.read()
            if ret is None or not ret:
                continue

            line1 = line(width, height)
            results, img = line1.check_line(frame)
            if (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1):
                line_find_flag =True
            cv2.imshow('Demo',img)
            k = cv2.waitKey(1)
            if k == 113 or k == 81:  # q or Q to quit
                print("Demo is quiting......")
                if not Develop_Mode:
                    controller.drive_dog("squat")
                cap.release()
                cv2.destroyWindow("Demo")
                stop_heartbeat = True
                is_line = False
                break

    line_recognize_thread = threading.Thread(target=line_recognize, args=())
    line_recognize_thread.start()

    global is_running
    is_running=True
    def run_control():
        global is_running
        global contest_process
        global sign
        while is_running:
            if contest_process ==0:
                controller.Velocity(7000, 25000, 0)
                time.sleep(11)
                controller.Velocity(0, 0, 0)
                time.sleep(1)
                controller.stairs_Mode()
                controller.Velocity(8000, 0, 0)
                time.sleep(7)
                controller.Move_Mode()
                controller.Stop()
                contest_process = contest_process + 1
            elif contest_process ==3:
                if sign =="turn left":
                    controller.Velocity(7000, 25000, 0)
                    time.sleep(11)
                    controller.Stop()
                elif sign =="turn right":
                    controller.Velocity(7000, -25000, 0)
                    time.sleep(11)
                    controller.Stop()

            is_running=False


    run_control_thread = threading.Thread(target=run_control, args=())
    run_control_thread.start()

    while True:
        if(stop_heartbeat):
            cv2.destroyWindow("Road Sign Recognition")
            break
        # if k == 113 or k == 81:  # q or Q to quit
        #     print("Demo is quiting......")
        #     if not Develop_Mode:
        #         controller.drive_dog("squat")
        #     cap.release()
        #     cv2.destroyWindow("Demo")
        #     stop_heartbeat = True
        #     is_line = False
        #     break
        ret1, frame1 = cap1.read()
        #ret1, frame1 = cap1.read()

        if ret1 is None or not ret1:
            continue

        # if ret1 is None or not ret1:
        #     continue

        height, width = frame1.shape[:2]


        if(contest_process==1):
            # line1 = line(width, height)
            # results, img = line1.check_line(frame)
            contest2_flag = True
            if(line_find_flag):
                print("find_line")
                contest_process = contest_process + 1
            else:
                controller.Velocity(8000, 0, 0)
                time.sleep(1)
                controller.Velocity(-8000, 0, 0)
                time.sleep(1)

        elif(contest_process==2):

            controller.Stop()
            if contest2_flag==True:
                controller.Velocity(8000, 0, 0)
                time.sleep(1)
                controller.Stop()
                contest2_flag =False

            bbox = sign_detector.detect(frame1)
            frame1 = sign_detector.visualize(frame1)
            sign = sign_detector.classify(frame1)

            image = frame1.copy()
            qcode_content = decodeDisplay(image)
            if qcode_content is not None and sign is not None:
                print("标志:{} ".format(sign))
                print("二维码:{} ".format(qcode_content))
                contest_process=contest_process+1
            cv2.imshow("Road Sign Recognition", frame1)
            cv2.waitKey(1)
            contest3_flag = True

        elif(contest_process==3):
            #cap1.release()
            cv2.destroyWindow("Road Sign Recognition")
            if contest3_flag==True:
                is_running==True
                contest3_flag=False





    # 打开视频文件
    # print("Wait 10 seconds and stand up......")
    # pack = struct.pack('<3i', 0x21010202, 0, 0)
    # Controller.send(pack)
    # time.sleep(5)
    # Controller.send(pack)
    # time.sleep(5)
    # Controller.send(pack)
    # print("Dog should stand up, otherwise press 'ctrl + c' and re-run the demo")

    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     print("succeed open video!")
    #     if not ret:
    #         print("dakai shibai ")
    #         break
    #     Controller.Velocity(0,0,30000,0,0)
    #     time.sleep(4)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     Controller.Velocity(8000,0, 0,0,0)
    #     time.sleep(0.5)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     Controller.Velocity(0,0,30000,0,0)
    #     time.sleep(4)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     while heise1_biaozhi == True:#第一个马路牙子
    #         ret, frame = cap.read()
    #         heise = 25
    #         if heise < 30:
    #             Controller.stairs_Mode()
    #             Controller.Velocity(10000, 0,0,0,0)
    #             time.sleep(6)
    #             Controller.Velocity(0,0,0,0,0)
    #             Controller.Move_Mode()
    #             heise1_biaozhi = False
    #             print("diyige maluyazi jieshu")
    #         else:
    #             Controller.Velocity(8000, 0, 0, 0, 0)
    #     Controller.Velocity(8000, 0,0, 0,0)
    #     time.sleep(0.5)
    #     cnt1 = 0
    #     while hengxian_biaozhi == True and cnt1 < 3 :#进入巡线，判断二维码，左右移动
    #         ret, frame = cap.read()
    #         results, img = line1.check_line(frame)
    #         if results[0]==1 and results[1]==1 and results[2]==1 and results[3] == 1 and results[4]==1:
    #             print("zhaodao xianle")
    #             Controller.Velocity(10000, 0, 0,0,0)
    #             time.sleep(1)
    #             hengxian_biaozhi = False
    #         else:
    #             Controller.Velocity(0, 8000, 0,0,0)
    #             cnt1 += 1
    #         Controller.Velocity(0, 0, 0, 0, 0)
    #     cnt2 = 0
    #     while lubiao != None:
    #         ret, frame = cap.read()
    #         lubiao = "left"
    #         cnt2 += 1
    #         if cnt2 > 10 :
    #             Controller.Velocity(0,8000,0,0,0)
    #             time.sleep(0.5)
    #             cnt2 = 0
    #
    #     Controller.Velocity(8000, 0, 0, 0, 0)
    #     time.sleep(0.5)
    #     if lubiao == "left":#左移
    #         Controller.Velocity(0, 0,30000, 0,0)
    #         time.sleep(8)
    #         Controller.Velocity(0,0,0,0,0)
    #         while zhixian1_biaozhi == True:#循迹直线
    #             ret, frame = cap.read()
    #             results ,img= check_line(frame)
    #             if results[2]  == 1:
    #                 Controller.Velocity(10000,0,0,0,0)
    #                 time.sleep(0.5)
    #                 zhixian1_biaozhi = False
    #             else:
    #                 id = 2
    #                 for i in Controller.turn_check_area:
    #                     if results[i] == 1:
    #                         id = i
    #                         break
    #                     if i <= 2:
    #                         Controller.Velocity(0,0, Controller.turn_vel[id], 0,0)
    #                     else:
    #                         Controller.Velocity(0, 0,0, Controller.turn_vel[id], 0)
    #         Controller.Velocity(0,0,0,0,0)
    #         Controller.stairs_Mode()
    #         Controller.Velocity(10000, 0, 0,0,0)
    #         time.sleep(6)
    #         Controller.Velocity(0,0,0,0,0)
    #         Controller.Move_Mode()
    #         while zhixian2_biaozhi == True:#越过马路牙子后再次巡线
    #             ret, frame = cap.read()
    #             results,img = check_line(frame)
    #             if results[2] == 0:
    #                 Controller.Velocity(0,0,0,0,0)
    #                 Controller.Velocity(0,0,0,30000,0)
    #                 time.sleep(8)
    #                 Controller.Velocity(0, 0, 0, 0, 0)
    #             else:
    #                 Controller.Velocity(8000,0,0,0,0)
    #         cnt3 = 0
    #         while hengxian2_biaozhi == True and cnt3 < 3:  # 进入巡线，判断二维码，左右移动
    #             ret, frame = cap.read()
    #             results, img = check_line(frame)
    #             if results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1:
    #                 print("zhaodao xianle")
    #                 Controller.Velocity(10000, 0, 0, 0, 0)
    #                 time.sleep(1)
    #                 hengxian2_biaozhi = False
    #             else:
    #                 Controller.Velocity(0, 8000, 0, 0, 0)
    #                 cnt3 += 1
    #             Controller.Velocity(0, 0, 0, 0, 0)
    #         Controller.Turn(0)
    #         time.sleep(1.5)
    #         Controller.Velocity(0,0,0,0,0)
    #         while zhixian3_biaozhi == True:#右转后循迹直线,调整
    #             results,img = check_line(frame)
    #             ret, frame = cap.read()
    #             if results[2] == 1:
    #                 Controller.Velocity(10000, 0, 0, 0, 0)
    #                 time.sleep(4)
    #                 Controller.Velocity(0, 0, 0, 0, 0)
    #                 zhixian3_biaozhi = False
    #             else:
    #                 id = 2
    #                 for i in Controller.turn_check_area:
    #                     if results[i] == 1:
    #                         id = i
    #                         break
    #                     if i <= 2:
    #                         Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
    #                     else:
    #                         Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
    #
    #     if lubiao == "Right":#右移
    #         Controller.Velocity(0, 0,0,30000,0)
    #         time.sleep(8)
    #         Controller.Velocity(0, 0, 0, 0, 0)
    #         while zhixian1_biaozhi == True:  # 循迹直线
    #             ret, frame = cap.read()
    #             results, img = check_line(frame)
    #             if results[2] == 1:
    #                 Controller.Velocity(10000, 0, 0, 0, 0)
    #                 time.sleep(4)
    #                 zhixian1_biaozhi = False
    #             else:
    #                 id = 2
    #                 for i in Controller.turn_check_area:
    #                     if results[i] == 1:
    #                         id = i
    #                         break
    #                     if i <= 2:
    #                         Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
    #                     else:
    #                         Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
    #         Controller.Velocity(0, 0, 0,0,0)
    #         while heise2_biaozhi == True:  # 第三个马路牙子
    #             ret, frame = cap.read()
    #             heise = check_heise(frame)
    #             if heise < 3:
    #                 heise2_biaozhi = False
    #                 Controller.Velocity(0, 0, 0, 0, 0)
    #                 Controller.stairs_Mode()
    #                 Controller.Velocity(10000, 0, 0, 0, 0)
    #                 time.sleep(6)
    #                 Controller.Velocity(0, 0, 0, 0, 0)
    #                 Controller.Move_Mode()
    #             else:
    #                 Controller.Velocity(8000, 0, 0, 0, 0)
    #         while T_biaozhi == True:#越过马路牙子后再次巡线,寻到T字路口左转
    #             ret, frame = cap.read()
    #             results,img = check_line(frame)
    #             if results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1 :
    #                 T_biaozhi = False
    #                 Controller.Velocity(8000, 0, 0,0,0)
    #                 time.sleep(0.5)
    #                 Controller.Velocity(0,0,0,0,0)
    #                 #前进一小段距离后左转
    #                 Controller.Turn(1)
    #                 time.sleep(1.5)
    #                 Controller.Velocity(0,0,0,0,0)
    #             else:
    #                 Controller.Velocity(8000, 0, 0, 0, 0)
    #         while zhixian2_biaozhi == True:  # 循迹直线
    #             ret, frame = cap.read()
    #             results, img = check_line(frame)
    #             if results[2] == 1:
    #                 Controller.Velocity(10000, 0, 0, 0, 0)
    #                 time.sleep(6)
    #                 zhixian2_biaozhi = False
    #             else:
    #                 id = 2
    #                 for i in Controller.turn_check_area:
    #                     if results[i] == 1:
    #                         id = i
    #                         break
    #                     if i <= 2:
    #                         Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
    #                     else:
    #                         Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
    #         Controller.Velocity(0, 0, 0, 0, 0)
    #
    #     while heise3_biaozhi == True:  # 第三个马路牙子
    #         ret, frame = cap.read()
    #         heise = check_heise(frame)
    #         if heise < 3:
    #             heise3_biaozhi = False
    #             Controller.Velocity(0, 0, 0, 0, 0)
    #             Controller.stairs_Mode()
    #             Controller.Velocity(10000, 0, 0, 0, 0)
    #             time.sleep(6)
    #             Controller.Velocity(0, 0, 0, 0, 0)
    #             Controller.Move_Mode()
    #         else:
    #             Controller.Velocity(8000, 0, 0, 0, 0)
    #     Controller.Velocity(10000, 0, 0, 0, 0)
    #     time.sleep(2)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     Controller.Velocity(0, 0, 30000, 0, 0)
    #     time.sleep(4)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     Controller.Velocity(8000, 0, 0, 0, 0)
    #     time.sleep(0.5)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     Controller.Velocity(0, 0, 30000, 0, 0)
    #     time.sleep(4)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     while zhixian4_biaozhi == True:  # 循迹直线
    #         ret, frame = cap.read()
    #         results, img = check_line(frame)
    #         if results[2] == 1:
    #             Controller.Velocity(10000, 0, 0, 0, 0)
    #             time.sleep(6)
    #             zhixian4_biaozhi = False
    #         else:
    #             id = 2
    #             for i in Controller.turn_check_area:
    #                 if results[i] == 1:
    #                     id = i
    #                     break
    #                 if i <= 2:
    #                     Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
    #                 else:
    #                     Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
    #     Controller.Velocity(0, 0, 0, 0, 0)
    #     # 处理当前帧
    #     results,img = check_line(frame)
    #
    #     # 输出结果
    #     print("结果：", results)
    #
    #     # 显示当前帧
    #     cv2.imshow('Frame', frame)
    #     cv2.imshow('gray', img)
    #
    #     # 检测键盘输入，按 'q' 键退出
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break
    #
    # # 释放资源
    # cap.release()
    # cv2.destroyAllWindows()