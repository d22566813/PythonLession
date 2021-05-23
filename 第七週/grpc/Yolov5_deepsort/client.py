import grpc

import track_pb2_grpc
import track_pb2
import pafy
import cv2
import numpy as np
# from PIL import Image
from numba import jit
# from io import BytesIO
# import base64
import time
import threading


class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False

        # 攝影機連接。
        self.capture = cv2.VideoCapture(URL)

    def start(self):
        # 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        # 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        # 當有需要影像時，再回傳最新的影像。
        return self.Frame.copy()

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()

        self.capture.release()


# 連接到 localhost:50051
channel = grpc.insecure_channel('localhost:50051')

# 創建一個 stub (gRPC client)
stub = track_pb2_grpc.TrackStub(channel)


func_status = {}
func_status['headpose'] = None
name = 'demo'
# "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66"
video = pafy.new(
    "https://www.youtube.com/watch?v=pFBsLTllFJo")
play = video.getbest(preftype="mp4")
cap = cv2.VideoCapture(play.url)
# https://www.youtube.com/watch?v=38R12C5xKWY&list=RDCMUC5HLreFwNngovwzB63lnpzg&index=10
# 連接攝影機
ipcam = ipcamCapture('rtsp://171.25.232.14/37edec0a09174c639e21c9fc4cf9d9a1')

# 啟動子執行緒
# ipcam.start()

# 暫停1秒，確保影像已經填充
# time.sleep(1)

# cap = cv2.VideoCapture('rtsp://admin:evro0811@89.21.77.183:33556/')
@jit(nopython=True)
def im_encode(im):
    success, encoded_image = cv2.imencode(".jpg", im)
    img_bytes = encoded_image.tobytes()
    return img_bytes
@jit(nopython=True)
def im_decode(im):
    return cv2.imdecode(np.frombuffer(
        im, np.uint8), -1)
    

now = time.time()
while True:

    # im = ipcam.getframe()
    (_, im) = cap.read()
    if im is None:
        break

    im = cv2.resize(im, (320, 180))
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    success, encoded_image = cv2.imencode(".jpg", im)
    img_bytes = encoded_image.tobytes()

    # img_bytes=im_encode(im)

    request = track_pb2.TrackRequest(image=img_bytes, label=[
                                     "person"], detect_type="Fence", point_array=[{'x': 0, 'y': 940},
                                                                                  {'x': 1919, 'y': 940}])
    response = stub.Track(request)

    # decoded=im_decode(response.algorithm_image)

    decoded = cv2.imdecode(np.frombuffer(
        response.algorithm_image, np.uint8), -1)

    cv2.imshow("demo", decoded)
    cv2.waitKey(1)

    now2 = time.time()
    print(now2-now)
    now = now2
