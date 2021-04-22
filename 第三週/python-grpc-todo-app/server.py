from concurrent import futures
import time

import grpc
import fence_pb2_grpc
import fence_pb2


import ai.fence_algorithm as fence_algorithm


# 創建一個 HelloServicer，要繼承自 hello_pb2_grpc.HelloServicer


class FenceServicer(fence_pb2_grpc.FenceServicer):

    # 由於我們 service 定義了 Hello 這個 rpc，所以要實作 Hello 這個 method
    def Fence(self, request, context):

        # response 是個 FenceResponse 形態的 message
        response = fence_pb2.FenceResponse()
        fence_result = fence_algorithm.fence_algorithm(
            request.inside, request.last_image, request.this_image)
        response.alert = fence_result.alert
        response.algorithm_image = fence_result.image
        return response


def serve():
    # 創建一個 gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# 利用 add_FenceServicer_to_server 這個 method 把上面定義的 HelloServicer 加到 server 當中
    fence_pb2_grpc.add_FenceServicer_to_server(FenceServicer(), server)

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
