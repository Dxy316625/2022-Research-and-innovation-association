import time
import struct
import cv2
import numpy as np
from controller import Controller
import threading

client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)

Controller = Controller(server_address)


cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
def heart_exchange(con):
    pack = struct.pack('<3i', 0x21040001, 0, 0)
    while True:
        con.send(pack)
        time.sleep(0.25)  # 4Hz

heart_exchange_thread = threading.Thread(target = heart_exchange, args = (Controller, ))
heart_exchange_thread.start() # 心跳


heise1_biaozhi = True
heise2_biaozhi = True
heise3_biaozhi = True
hengxian_biaozhi =True
hengxian2_biaozhi =True
zhixian1_biaozhi = True
zhixian2_biaozhi = True
zhixian3_biaozhi = True
zhixian4_biaozhi = True
zuoyi_biaozhi = True
zhongdian_biaozhi = True
T_biaozhi = True


ret, frame = cap.read()
if not ret:
    print("Failed to read video frame.")
    exit()

height, width = frame.shape[:2]
cap.release()


def check_line(frame):
    length = width // 5
    begin_y = height - length
    end_y = height

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 应用全局阈值进行二值化
    _, binary_img = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # 对二值图像进行膨胀
    kernel = np.ones((5, 5), np.uint8)
    dilated_img = cv2.dilate(binary_img, kernel, iterations=1)

    # 存储结果的数组
    results = []

    # 计算每个 ROI 区域中白色像素的数量
    for i in range(1, 6):
        begin_x = (i - 1) * length
        end_x = i * length

        # 提取 ROI 区域
        roi_img = dilated_img[begin_y :end_y, begin_x:end_x,:]

        # 计算白色像素的数量
        white_pixels = np.count_nonzero(roi_img == 255)

        # 如果白色像素数量大于区域面积的 10%，则为 1，否则为 0
        if white_pixels > 0.1 * length * length:
            results.append(1)
        else:
            results.append(0)

    return results, binary_img

def check_heise(img):
    result = 1
    return result

def check_lubiao(img):
    result = "left"
    return result

global lubiao

if __name__ == '__main__':
    # 打开视频文件
    print("Wait 10 seconds and stand up......")
    pack = struct.pack('<3i', 0x21010202, 0, 0)
    Controller.send(pack)
    time.sleep(5)
    Controller.send(pack)
    time.sleep(5)
    Controller.send(pack)
    print("Dog should stand up, otherwise press 'ctrl + c' and re-run the demo")

    while cap.isOpened():
        ret, frame = cap.read()
        print("succeed open video!")
        if not ret:
            print("dakai shibai ")
            break
        Controller.Velocity(0,0,30000,0,0)
        time.sleep(4)
        Controller.Velocity(0, 0, 0, 0, 0)
        Controller.Velocity(8000,0, 0,0,0)
        time.sleep(0.5)
        Controller.Velocity(0, 0, 0, 0, 0)
        Controller.Velocity(0,0,30000,0,0)
        time.sleep(4)
        Controller.Velocity(0, 0, 0, 0, 0)
        while heise1_biaozhi == True:#第一个马路牙子
            ret, frame = cap.read()
            heise = check_heise(frame)
            if heise < 30:
                Controller.stairs_Mode()
                Controller.Velocity(10000, 0,0,0,0)
                time.sleep(6)
                Controller.Velocity(0,0,0,0,0)
                Controller.Move_Mode()
                heise1_biaozhi = False
                print("diyige maluyazi jieshu")
            else:
                Controller.Velocity(8000, 0, 0, 0, 0)
        Controller.Velocity(8000, 0,0, 0,0)
        time.sleep(0.5)
        cnt1 = 0
        while hengxian_biaozhi == True and cnt1 < 3 :#进入巡线，判断二维码，左右移动
            ret, frame = cap.read()
            results, img = check_line(frame)
            if results[0]==1 and results[1]==1 and results[2]==1 and results[3] == 1 and results[4]==1:
                print("zhaodao xianle")
                Controller.Velocity(10000, 0, 0,0,0)
                time.sleep(1)
                hengxian_biaozhi = False
            else:
                Controller.Velocity(0, 8000, 0,0,0)
                cnt1 += 1
            Controller.Velocity(0, 0, 0, 0, 0)
        cnt2 = 0
        while lubiao != None:
            ret, frame = cap.read()
            lubiao = check_lubiao(frame)
            cnt2 += 1
            if cnt2 > 10 :
                Controller.Velocity(0,8000,0,0,0)
                time.sleep(0.5)
                cnt2 = 0

        Controller.Velocity(8000, 0, 0, 0, 0)
        time.sleep(0.5)
        if lubiao == "left":#左移
            Controller.Velocity(0, 0,30000, 0,0)
            time.sleep(8)
            Controller.Velocity(0,0,0,0,0)
            while zhixian1_biaozhi == True:#循迹直线
                ret, frame = cap.read()
                results ,img= check_line(frame)
                if results[2]  == 1:
                    Controller.Velocity(10000,0,0,0,0)
                    time.sleep(0.5)
                    zhixian1_biaozhi = False
                else:
                    id = 2
                    for i in Controller.turn_check_area:
                        if results[i] == 1:
                            id = i
                            break
                        if i <= 2:
                            Controller.Velocity(0,0, Controller.turn_vel[id], 0,0)
                        else:
                            Controller.Velocity(0, 0,0, Controller.turn_vel[id], 0)
            Controller.Velocity(0,0,0,0,0)
            Controller.stairs_Mode()
            Controller.Velocity(10000, 0, 0,0,0)
            time.sleep(6)
            Controller.Velocity(0,0,0,0,0)
            Controller.Move_Mode()
            while zhixian2_biaozhi == True:#越过马路牙子后再次巡线
                ret, frame = cap.read()
                results,img = check_line(frame)
                if results[2] == 0:
                    Controller.Velocity(0,0,0,0,0)
                    Controller.Velocity(0,0,0,30000,0)
                    time.sleep(8)
                    Controller.Velocity(0, 0, 0, 0, 0)
                else:
                    Controller.Velocity(8000,0,0,0,0)
            cnt3 = 0
            while hengxian2_biaozhi == True and cnt3 < 3:  # 进入巡线，判断二维码，左右移动
                ret, frame = cap.read()
                results, img = check_line(frame)
                if results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1:
                    print("zhaodao xianle")
                    Controller.Velocity(10000, 0, 0, 0, 0)
                    time.sleep(1)
                    hengxian2_biaozhi = False
                else:
                    Controller.Velocity(0, 8000, 0, 0, 0)
                    cnt3 += 1
                Controller.Velocity(0, 0, 0, 0, 0)
            Controller.Turn(0)
            time.sleep(1.5)
            Controller.Velocity(0,0,0,0,0)
            while zhixian3_biaozhi == True:#右转后循迹直线,调整
                results,img = check_line(frame)
                ret, frame = cap.read()
                if results[2] == 1:
                    Controller.Velocity(10000, 0, 0, 0, 0)
                    time.sleep(4)
                    Controller.Velocity(0, 0, 0, 0, 0)
                    zhixian3_biaozhi = False
                else:
                    id = 2
                    for i in Controller.turn_check_area:
                        if results[i] == 1:
                            id = i
                            break
                        if i <= 2:
                            Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
                        else:
                            Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)

        if lubiao == "Right":#右移
            Controller.Velocity(0, 0,0,30000,0)
            time.sleep(8)
            Controller.Velocity(0, 0, 0, 0, 0)
            while zhixian1_biaozhi == True:  # 循迹直线
                ret, frame = cap.read()
                results, img = check_line(frame)
                if results[2] == 1:
                    Controller.Velocity(10000, 0, 0, 0, 0)
                    time.sleep(4)
                    zhixian1_biaozhi = False
                else:
                    id = 2
                    for i in Controller.turn_check_area:
                        if results[i] == 1:
                            id = i
                            break
                        if i <= 2:
                            Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
                        else:
                            Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
            Controller.Velocity(0, 0, 0,0,0)
            while heise2_biaozhi == True:  # 第三个马路牙子
                ret, frame = cap.read()
                heise = check_heise(frame)
                if heise < 3:
                    heise2_biaozhi = False
                    Controller.Velocity(0, 0, 0, 0, 0)
                    Controller.stairs_Mode()
                    Controller.Velocity(10000, 0, 0, 0, 0)
                    time.sleep(6)
                    Controller.Velocity(0, 0, 0, 0, 0)
                    Controller.Move_Mode()
                else:
                    Controller.Velocity(8000, 0, 0, 0, 0)
            while T_biaozhi == True:#越过马路牙子后再次巡线,寻到T字路口左转
                ret, frame = cap.read()
                results,img = check_line(frame)
                if results[0] == 1 and results[1] == 1 and results[2] == 1 and results[3] == 1 and results[4] == 1 :
                    T_biaozhi = False
                    Controller.Velocity(8000, 0, 0,0,0)
                    time.sleep(0.5)
                    Controller.Velocity(0,0,0,0,0)
                    #前进一小段距离后左转
                    Controller.Turn(1)
                    time.sleep(1.5)
                    Controller.Velocity(0,0,0,0,0)
                else:
                    Controller.Velocity(8000, 0, 0, 0, 0)
            while zhixian2_biaozhi == True:  # 循迹直线
                ret, frame = cap.read()
                results, img = check_line(frame)
                if results[2] == 1:
                    Controller.Velocity(10000, 0, 0, 0, 0)
                    time.sleep(6)
                    zhixian2_biaozhi = False
                else:
                    id = 2
                    for i in Controller.turn_check_area:
                        if results[i] == 1:
                            id = i
                            break
                        if i <= 2:
                            Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
                        else:
                            Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
            Controller.Velocity(0, 0, 0, 0, 0)

        while heise3_biaozhi == True:  # 第三个马路牙子
            ret, frame = cap.read()
            heise = check_heise(frame)
            if heise < 3:
                heise3_biaozhi = False
                Controller.Velocity(0, 0, 0, 0, 0)
                Controller.stairs_Mode()
                Controller.Velocity(10000, 0, 0, 0, 0)
                time.sleep(6)
                Controller.Velocity(0, 0, 0, 0, 0)
                Controller.Move_Mode()
            else:
                Controller.Velocity(8000, 0, 0, 0, 0)
        Controller.Velocity(10000, 0, 0, 0, 0)
        time.sleep(2)
        Controller.Velocity(0, 0, 0, 0, 0)
        Controller.Velocity(0, 0, 30000, 0, 0)
        time.sleep(4)
        Controller.Velocity(0, 0, 0, 0, 0)
        Controller.Velocity(8000, 0, 0, 0, 0)
        time.sleep(0.5)
        Controller.Velocity(0, 0, 0, 0, 0)
        Controller.Velocity(0, 0, 30000, 0, 0)
        time.sleep(4)
        Controller.Velocity(0, 0, 0, 0, 0)
        while zhixian4_biaozhi == True:  # 循迹直线
            ret, frame = cap.read()
            results, img = check_line(frame)
            if results[2] == 1:
                Controller.Velocity(10000, 0, 0, 0, 0)
                time.sleep(6)
                zhixian4_biaozhi = False
            else:
                id = 2
                for i in Controller.turn_check_area:
                    if results[i] == 1:
                        id = i
                        break
                    if i <= 2:
                        Controller.Velocity(0, 0, Controller.turn_vel[id], 0, 0)
                    else:
                        Controller.Velocity(0, 0, 0, Controller.turn_vel[id], 0)
        Controller.Velocity(0, 0, 0, 0, 0)
        # 处理当前帧
        results,img = check_line(frame)

        # 输出结果
        print("结果：", results)

        # 显示当前帧
        cv2.imshow('Frame', frame)
        cv2.imshow('gray', img)

        # 检测键盘输入，按 'q' 键退出
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
