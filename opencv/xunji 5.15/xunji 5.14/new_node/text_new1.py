import time
import struct
import cv2
from controller import Controller
from qcode_detect import decodeDisplay
from RoadSignRecognition import RoadSignRecognition
import threading
from line import line

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
is_line_flag=False
is_capture_flag=False
contest_process=0
qcode_content=None
sign =None
is_capture=True

is_running =True
is_running_flag=True
run_cnt=0


if __name__ == '__main__':
    sign_detector = RoadSignRecognition()
    controller = Controller(server_address)
    stop_heartbeat = False

    if Develop_Mode:
        cap = cv2.VideoCapture(0)
        # cap1 = cv2.VideoCapture(1)
    # from Robot Dog
    else:
        cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)
        #cap1 = cv2.VideoCapture("/dev/video6", cv2.CAP_V4L2)
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



    global results
    global img

    line_find_flag = False


    def run_control():
        global is_running
        global contest_process
        global sign
        global is_running_flag
        cnt=0
        qianjin=0
        zuoyou=0
        while is_running:
            while is_running_flag:
                if contest_process ==0:
                    controller.Velocity(7000, 25000, 0)
                    time.sleep(10)
                    controller.Velocity(0, 0, 0)
                    time.sleep(1)
                    controller.stairs_Mode()
                    controller.Velocity(8000, 0, 0)
                    time.sleep(8)
                    controller.Walk_Mode()
                    controller.Stop()
                    contest_process = contest_process + 1
                    is_running_flag = False
                elif contest_process==1:
                    # controller.Velocity(8000, 0, 0)
                    # time.sleep(1)
                    # controller.Velocity(-8000, 0, 0)
                    # time.sleep(1)
                    controller.Stop()
                    time.sleep(1)
                    controller.Velocity(8000, 13000, 0)

                elif contest_process ==3:
                    #print(sign)
                    if sign =="turn left":
                        print(cnt)

                        ret, frame = cap.read()
                        if ret is None or not ret:
                            continue
                        height, width = frame.shape[:2]

                        line1 = line(width, height)
                        results, img = line1.check_line(frame)
                        print(results)

                        if cnt == 0:
                            controller.Turn(1)
                            time.sleep(1)
                            controller.Stop()
                            controller.Walk_Mode()
                            cnt = 1
                        elif cnt == 6:
                            controller.Stop()
                            is_running_flag = False
                            continue
                        if (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 0 and results[4] == 0):
                            qianjin = 8800
                            zuoyou = 0
                        elif (results[0] == 0 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            qianjin = 7800
                            zuoyou = 17000  # 17000~20000(左为正，右为负)
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            qianjin = 7300
                            zuoyou = 18500  # 17000~20000(左为正，右为负)
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[4] == 0):
                            qianjin = 7800
                            zuoyou = -17000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[4] == 1):
                            qianjin = 7300
                            zuoyou = -18500
                        elif (results[0] == 1 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            qianjin = 7000
                            zuoyou = 20000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[4] == 1):
                            qianjin = 7000
                            zuoyou = -20000
                        elif (results[0] == 1 and results[1] == 1 and results[3] == 0 and results[4] == 0):
                            controller.Walk_Mode()
                            if cnt == 5:
                                controller.Velocity(7500, 0, 0)
                                time.sleep(3)
                                controller.Turn(1)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                cnt = 6
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1):
                            time.sleep(1.5)
                            controller.Velocity(0, 0, 0)
                            time.sleep(1)
                            controller.Turn(1)
                            time.sleep(1.1)
                            controller.Velocity(7000, 0, 0)
                            if cnt == 3:
                                cnt = 4
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            print(cnt)
                            time.sleep(1)
                            if cnt == 1:
                                print("hhh")
                                controller.Velocity(9000, 0, 0)
                                time.sleep(2.5)
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                cnt = 2
                            elif cnt == 2:
                                controller.Walk_Mode()
                                controller.Velocity(7000, 20000, 0)
                                time.sleep(8)
                                controller.Velocity(7500, 0, 0)
                                cnt = 3
                            elif cnt == 4:
                                print("hhh")
                                controller.stairs_Mode()
                                controller.Velocity(9000, 0, 0)
                                time.sleep(2.5)
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                cnt = 5
                            elif cnt == 7:
                                time.sleep(2)
                                controller.Stop()
                                contest_process = 4
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 1 and results[4] == 1):
                            print(1)
                            if cnt == 0:
                                time.sleep(1.8)
                                controller.Turn(0)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                controller.stairs_Mode()
                                time.sleep(1)
                                cnt = 1
                            elif cnt == 6:
                                time.sleep(1.8)
                                controller.Walk_Mode()
                                controller.Turn(0)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                cnt = 7

                        controller.Velocity(qianjin, zuoyou, 0)


                    elif sign =="turn right":
                        print(cnt)

                        ret, frame = cap.read()
                        if ret is None or not ret:
                            continue
                        height, width = frame.shape[:2]

                        line1 = line(width, height)
                        results, img = line1.check_line(frame)
                        print(results)

                        if cnt==0:
                            controller.Velocity(7500,0,0)
                            time.sleep(2)
                            controller.Turn(0)
                            time.sleep(1)
                            controller.Stop()
                            controller.Walk_Mode()
                            cnt=1

                        elif cnt==6:
                            controller.Stop()
                            is_running_flag=False
                            continue


                        if (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 0 and results[4] == 0):
                            qianjin=8800
                            zuoyou=0
                        elif (results[0] == 0 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            qianjin =7800
                            zuoyou = 17000     #17000~20000(左为正，右为负)
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            qianjin =7300
                            zuoyou = 18500     #17000~20000(左为正，右为负)
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[4] == 0):
                            qianjin = 7800
                            zuoyou = -17000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 1 and results[4] == 1):
                            qianjin = 7300
                            zuoyou = -18500
                        elif (results[0] == 1 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            qianjin = 7000
                            zuoyou = 20000
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[4] == 1):
                            qianjin = 7000
                            zuoyou = -20000
                        elif (results[0] == 1 and results[1] == 1  and results[2] == 1 and results[3] == 0 and results[4] == 0):
                            controller.Walk_Mode()
                            if cnt == 1:
                                controller.Velocity(8500, 0, 0)
                                time.sleep(2)
                                controller.Turn(1)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                controller.stairs_Mode()
                                time.sleep(1)
                                cnt = 2
                            elif cnt == 4:
                                controller.Velocity(8500, 0, 0)
                                time.sleep(3)
                                controller.Turn(1)
                                time.sleep(1)
                                controller.Velocity(0, 0, 0)
                                cnt = 5
                        elif (results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1):
                            time.sleep(1.3)
                            controller.Velocity(0, 0, 0)
                            controller.Walk_Mode()
                            time.sleep(1)
                            controller.Velocity(7500, 0, 0)
                            time.sleep(2)
                            controller.Turn(1)
                            time.sleep(1)
                            controller.Velocity(7000, 0, 0)
                            if cnt == 2:
                                cnt = 3
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 0 and results[3] == 0 and results[4] == 0):
                            print(cnt)
                            if cnt == 3:
                                print("hhh")
                                controller.stairs_Mode()
                                controller.Velocity(9000, 0, 0)
                                time.sleep(2.5)
                                controller.Velocity(0, 0, 0)
                                time.sleep(1)
                                cnt = 4
                            #elif cnt == 5:
                                #time.sleep(2)
                                #controller.Stop()
                                #cnt = 6
                        elif (results[0] == 0 and results[1] == 0 and results[2] == 1 and results[3] == 1):
                            if cnt == 5:
                                controller.Walk_Mode()
                                time.sleep(1)
                                controller.Turn(0)
                                time.sleep(1)
                                controller.Velocity(9000, 0, 0)
                                time.sleep(3)
                                cnt=6
                        controller.Velocity(int(qianjin), int(zuoyou), 0)



                if stop_heartbeat:
                    break
            if stop_heartbeat:
                break


    run_control_thread = threading.Thread(target=run_control, args=())
    run_control_thread.start()
    controller.Move_Mode()

    while True:
        if(stop_heartbeat):
            is_capture = False
            is_line = False
            break
        #print(contest_process)
        #time.sleep(1)


        if(contest_process==1):
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
                contest_process = contest_process + 1
                is_running_flag = False
                # time.sleep(2)
                controller.Velocity(8000, 0, 0)
                time.sleep(3.5)
                controller.Stop()
                controller.stand_Mode()
                controller.Velocity(-32768, 0, 0)

                # cv2.destroyWindow("Demo")

                continue
            else:
                is_running_flag=True
                # controller.Velocity(8000, 0, 0)
                # time.sleep(1)
                # controller.Velocity(-8000, 0, 0)
                # time.sleep(1)



            # is_line_flag = True

            # if(line_find_flag):
            #     print("find_line")
            #     contest_process = contest_process + 1


        elif(contest_process==2):



            #
            contest3_flag = True
            ret, frame = cap.read()
            if ret is None or not ret:
                continue

            bbox = sign_detector.detect(frame)
            frame = sign_detector.visualize(frame)
            sign = sign_detector.classify(frame)

            # print(is_capture_flag)
            #print(frame)
            # if is_capture_flag:
            cv2.imshow("Demo", frame)
            image = frame.copy()
            if qcode_content==None:
                qcode_content = decodeDisplay(image)
            if qcode_content is not None and sign is not None:
                print("标志:{} ".format(sign))
                print("二维码:{} ".format(qcode_content))
                # is_capture_flag = False
                controller.Move_Mode()
                controller.Walk_Mode()
                # cv2.destroyWindow("Road Sign Recognition")
                contest_process = contest_process + 1



        elif(contest_process==3):
            #cap1.release()
            #cv2.destroyWindow("Road Sign Recognition")
            # print(is_running_flag)
            if contest3_flag==True:
                is_running_flag=True
                contest3_flag=False

            ret, frame = cap.read()
            if ret is None or not ret:
                continue
            height, width = frame.shape[:2]

            line1 = line(width, height)
            results, img = line1.check_line(frame)
            cv2.imshow('Demo', img)




        k = cv2.waitKey(1)
        if k == 113 or k == 81:  # q or Q to quit
            print("Demo is quiting......")
            if not Develop_Mode:
                controller.drive_dog("squat")
            cap.release()
            cv2.destroyWindow("Demo")
            stop_heartbeat = True
            # is_line = False
            is_running=False
            break
