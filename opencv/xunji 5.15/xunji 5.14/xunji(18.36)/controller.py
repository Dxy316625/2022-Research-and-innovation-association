import socket
import struct


class Controller:
    def __init__(self, dst):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dst = dst

    # 发消息咯
    def send(self, pack):
        self.socket.sendto(pack, self.dst)

    # 速度
    def Velocity(self, forward_back, left_right, rotate):
        msg1 = struct.pack('<3i', 0x21010130, forward_back, 0)
        self.send(msg1)
        msg2 = struct.pack('<3i', 0x21010131, -left_right, 0)
        self.send(msg2)
        msg3 = struct.pack('<3i', 0x21010135, rotate, 0)
        self.send(msg3)
        print("Change Velocity to LeftRight: %d, ForwardBack: %d, Rotate: %d" % (left_right, forward_back, rotate))

    def Stop(self):
        self.Velocity(0, 0, 0)

    # 转弯
    def Turn(self, direction):
        basic_turn_velocity = 16384
        if (direction == 0):
            self.Velocity(0, 0, basic_turn_velocity)
        elif (direction == 1):
            self.Velocity(0, 0, -basic_turn_velocity)
        # 0 右转 1 左转

    MAX_VEL = int(32767)
    basic_vel = int(MAX_VEL // 2)
    turn_vel = [int(basic_vel / 0.9), int(basic_vel), int(0), int(basic_vel), int(basic_vel / 0.9)]
    turn_check_area = [2, 1, 3, 0, 4]

    def Walk_Mode(self):
        # 行走模式
        msg = struct.pack('<3i', 0x21010300, 0, 0)
        self.send(msg)
        print("Change to Walk Mode")


    def Move_Mode(self):
        # 移动模式
        msg = struct.pack('<3i', 0x21010D06, 0, 0)
        self.send(msg)
        print("Change to Move Mode")

    def stairs_Mode(self):
        # 楼梯模式
        msg = struct.pack('<3i', 0x21010401, 0, 0)
        self.send(msg)
        print("Change to stairs Mode")


    def stand_Mode(self):
        #站立
        msg = struct.pack('<3i', 0x21010D05, 0, 0)
        self.send(msg)
        print("Change to stand Mode")

    # def up_Mode(self):
    #     # 站立
    #     msg = struct.pack('<3i', 0x21010D05, 0, 0)
    #     self.send(msg)
    #     print("Change to stand Mode")