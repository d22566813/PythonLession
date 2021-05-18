import grpc

import track_pb2_grpc
import track_pb2
import pafy
import cv2
import numpy as np

# 連接到 localhost:50051
channel = grpc.insecure_channel('localhost:50051')

# 創建一個 stub (gRPC client)
stub = track_pb2_grpc.TrackStub(channel)


func_status = {}
func_status['headpose'] = None
name = 'demo'

video = pafy.new(
    "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66")
play = video.getbest(preftype="mp4")
cap = cv2.VideoCapture(play.url)

while True:
    (_, im) = cap.read()
    if im is None:
        break
    # im = cv2.resize(im, (960, 540))

    # cv2.imshow("demo", im)
    # cv2.waitKey(1)

    success, encoded_image = cv2.imencode(".jpg", im)
    img_bytes = encoded_image.tostring()

    request = track_pb2.TrackRequest(image=img_bytes)
    response = stub.Track(request)
    decoded = cv2.imdecode(np.frombuffer(
        response.algorithm_image, np.uint8), -1)

    # decoded = cv2.imdecode(np.frombuffer(
    #     img_bytes, np.uint8), -1)

    cv2.imshow("demo", decoded)
    cv2.waitKey(1)
