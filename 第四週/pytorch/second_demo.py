import cv2
import torch
from PIL import Image
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Images
# for f in ['zidane.jpg', 'bus.jpg']:  # download 2 images
#     print(f'Downloading {f}...')
#     torch.hub.download_url_to_file(
#         'https://github.com/ultralytics/yolov5/releases/download/v1.0/' + f, f)
img1 = Image.open('zidane.jpg')  # PIL image
img2 = cv2.imread('bus.jpg')[:, :, ::-1]  # OpenCV image (BGR to RGB)
imgs = [img1, img2]  # batch of images

# Inference
results = model(imgs, size=640)  # includes NMS

# Results
results.print()
# results.save()  # or .show()
# results.show()  # or .show()

# results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)
