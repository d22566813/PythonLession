import track_pb2
import track_pb2_grpc
import grpc
import time
from concurrent import futures
from AIDetector_pytorch import Detector
import numpy as np
import cv2
import imutils

# 創建一個 HelloServicer，要繼承自 hello_pb2_grpc.HelloServicer


def img_to_numpy_arr(mat_bytes):
    """
    圖片轉成Numpy陣列
    """
    nparr = np.frombuffer(mat_bytes, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return nparr


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


class TrackServicer(track_pb2_grpc.TrackServicer):
    def __init__(self):
        self.func_status = {}
        self.func_status['headpose'] = None
        self.detect = Detector()
    # 由於我們 service 定義了 Hello 這個 rpc，所以要實作 Hello 這個 method

    def Track(self, request, context):

        # response 是個 FenceResponse 形態的 message
        response = track_pb2.TrackResponse()
        image_np = img_to_numpy_arr(request.image)

        # image_array = cv2.imdecode(np.frombuffer(
        #     request.image, np.uint8), -1)

        # track_result = self.detect.feedCap(image_array, self.func_status)
        # track_result = track_result['frame']
        # track_result = imutils.resize(track_result, height=500)
        # success, encoded_image = cv2.imencode(".jpg", track_result)

        self.detect.feedCap(image_np, self.func_status, request.label)

        # image_array = cv2.resize(image_array, (960, 540))

        # success, encoded_image = cv2.imencode(".jpg", image_array)

        # img_bytes = encoded_image.tostring()

        # response.algorithm_image = img_bytes

        response.algorithm_image = numpy_arr_to_img(image_np)

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
