import grpc

import track_pb2_grpc
import track_pb2
import pafy
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import time

# 連接到 localhost:50051
channel = grpc.insecure_channel('localhost:50051')

# 創建一個 stub (gRPC client)
stub = track_pb2_grpc.TrackStub(channel)


func_status = {}
func_status['headpose'] = None
name = 'demo'
# "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66"
video = pafy.new("https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66"
                 )
play = video.getbest(preftype="mp4")
# cap = cv2.VideoCapture(play.url)

cap = cv2.VideoCapture('rtsp://171.25.232.14/37edec0a09174c639e21c9fc4cf9d9a1')


def img_to_numpy_arr(mat_bytes):
    """
    圖片轉成Numpy陣列
    """

    mat = base64.b64decode(mat_bytes)
    nparr = np.frombuffer(mat, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def numpy_arr_to_img(arr):
    """
    Numpy陣列轉成圖片
    """
    pil_img = Image.fromarray(arr)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")

    # img = base64.b64encode(buff.getvalue()).decode('utf-8')
    # return img
    return buff.getvalue()


now = time.time()
while True:

    (_, im) = cap.read()
    if im is None:
        break

    # img_bytes = numpy_arr_to_img(im)
    im = cv2.resize(im, (1920, 1080))

    # cv2.imshow("demo", im)
    # cv2.waitKey(1)

    success, encoded_image = cv2.imencode(".jpg", im)
    img_bytes = encoded_image.tobytes()

    request = track_pb2.TrackRequest(image=img_bytes, label=[
                                     "person"], detect_type="Fence", point_array=[{'x': 0, 'y': 940},
                                                                                  {'x': 1919, 'y': 940}])
    response = stub.Track(request)
    # decoded = cv2.imdecode(np.frombuffer(
    #     response.algorithm_image, np.uint8), -1)

    # decoded = cv2.imdecode(np.frombuffer(
    #     img_bytes, np.uint8), -1)

    # img_show = img_to_numpy_arr(img_bytes)

    now2 = time.time()
    print(now2-now)
    now = now2
    cv2.imshow("demo", im)
    cv2.waitKey(1)
