import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Image
img = 'https://github.com/ultralytics/yolov5/raw/master/data/images/bus.jpg'

# Inference
results = model(img)
