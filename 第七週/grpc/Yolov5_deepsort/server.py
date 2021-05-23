import track_pb2
import track_pb2_grpc
import grpc
import time
from concurrent import futures
from AIDetector_pytorch import Detector
import numpy as np
import cv2
# import imutils
# import mxnet as mx


# 創建一個 HelloServicer，要繼承自 hello_pb2_grpc.HelloServicer


class TrackServicer(track_pb2_grpc.TrackServicer):
    def __init__(self):
        self.func_status = {}
        self.func_status['headpose'] = None
        self.detect = Detector()
    # 由於我們 service 定義了 Hello 這個 rpc，所以要實作 Hello 這個 method

    def Track(self, request, context):

        # response 是個 FenceResponse 形態的 message
        response = track_pb2.TrackResponse()

        image_array = cv2.imdecode(np.frombuffer(
            request.image, np.uint8), -1)

        # image_array = mx.image.imdecode(np.frombuffer(
        #     request.image, np.uint8))
        # image_array = image_array.asnumpy()

        image_array = self.detect.feedCap(
            image_array, self.func_status, request.label)
        image_array = image_array['frame']

        # image_array = imutils.resize(image_array, height=500)

        success, encoded_image = cv2.imencode(".jpg", image_array)

        img_bytes = encoded_image.tobytes()

        response.algorithm_image = img_bytes

        # response.algorithm_image = request.image

        return response


def serve():
    # 創建一個 gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# 利用 add_FenceServicer_to_server 這個 method 把上面定義的 HelloServicer 加到 server 當中
    track_pb2_grpc.add_TrackServicer_to_server(
        TrackServicer(), server)

# 讓 server 跑在 port 50051 中
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
