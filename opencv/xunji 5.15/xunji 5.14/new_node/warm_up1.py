import time
import struct
import cv2
from controller import Controller
import threading



client_address = ("192.168.1.103", 43897)
server_address = ("192.168.1.120", 43893)
Develop_Mode = False



if __name__ == '__main__':
    controller = Controller(server_address)
    stop_heartbeat = False


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
   
    time.sleep(2)

    controller.Velocity(7000, -25000, 0)
    time.sleep(2)
    controller.Stop()

    
    controller.drive_dog("squat")
