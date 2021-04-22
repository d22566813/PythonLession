import grpc

import fence_pb2_grpc
import fence_pb2

# 連接到 localhost:50051
channel = grpc.insecure_channel('localhost:50051')

# 創建一個 stub (gRPC client)
stub = fence_pb2_grpc.FenceStub(channel)

# 創建一個 HelloRequest 丟到 stub 去
request = fence_pb2.FenceRequest(inside=1, last_image=b'', this_image=b'')

# 呼叫 Hello service，回傳 HelloResponse
response = stub.Fence(request)

print(response.alert)
print(response.algorithm_image)
