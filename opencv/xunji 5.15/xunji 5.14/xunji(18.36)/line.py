import cv2
import numpy as np


class line:
    def __init__(self,width,height):
        self.width = width
        self.height =height

    def check_line(self,frame):
        length = self.width // 5
        begin_y = self.height - length
        end_y = self.height

        # 转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 应用全局阈值进行二值化
        _, binary_img = cv2.threshold(gray, 248, 255, cv2.THRESH_BINARY)

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
            roi_img = dilated_img[begin_y:end_y, begin_x:end_x]

            # 计算白色像素的数量
            white_pixels = np.count_nonzero(roi_img == 255)

            # 如果白色像素数量大于区域面积的 10%，则为 1，否则为 0
            if white_pixels > 0.15 * length * length:
                results.append(1)
            else:
                results.append(0)

        return results, binary_img


