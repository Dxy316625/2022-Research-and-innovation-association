import cv2
import pyzbar.pyzbar as pyzbar
#import numpy as np
#from PIL import Image, ImageDraw, ImageFont


def decodeDisplay(video):
    # qrCodeDetector = cv2.QRCodeDetector()
    # gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    # data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(gray)
    # return data

    #gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray)  # 对比度增强
    #gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯锐化
    barcodes = pyzbar.decode(video)
    for barcode in barcodes:
        #(x, y, w, h) = barcode.rect  # 提取二维码的位置,然后用边框标识出来在视频中
        #cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 0), 2)
        barcodeData = barcode.data.decode("utf-8")  # 字符串转换
        #barcodeType = barcode.type
        # 在图像上面显示识别出来的内容   #不能显示中文
        # text = "{}".format(barcodeData)
        # cv2.putText(video, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
        #img_PIL = Image.fromarray(cv2.cvtColor(video, cv2.COLOR_BGR2RGB))
        #font = ImageFont.truetype('font/simsun.ttc', 35)  # 参数（字体，大小）
        #fillColor = (0, 255, 255)  # 字体颜色（rgb)
        #position = (x, y - 50)  # 文字输出位置
        #str = barcodeData  # 输出内容
        #draw = ImageDraw.Draw(img_PIL)
        #draw.text(position, str, font=font, fill=fillColor)
        #video = np.array(img_PIL)
        #print("[扫描结果] 二维码类别： {0} 内容： {1}".format(barcodeType, barcodeData))
        return barcodeData
    #cv2.imshow("Demo", video)




