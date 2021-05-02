import cv2
import pafy
import torch
import os
import argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    # yolov5
    parser.add_argument('--weights', nargs='+', type=str,
                        default='./weights/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--img-size', type=int, default=960,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.4, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.5, help='IOU threshold for NMS')
    parser.add_argument(
        '--classes', default=[0], type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')

    return parser.parse_args()


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

args = parse_args()
print(args)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', args)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# model.cuda()
model.to(device)

stream_url = [
    "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66",
    "https://www.youtube.com/watch?v=HUbQTGraucg",
    "https://www.youtube.com/watch?v=EkrZJrYqWFE"
]
# video = pafy.new(
#     "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66")

# video = pafy.new(
#     "https://www.youtube.com/watch?v=HUbQTGraucg")

# video = pafy.new(
#     "https://www.youtube.com/watch?v=EkrZJrYqWFE")

# play = video.getbest(preftype="mp4")

# stream = cv2.VideoCapture(play.url)
stream = []
for s in stream_url:
    video = pafy.new(s)
    play = video.getbest(preftype="mp4")
    stream.append(cv2.VideoCapture(play.url))

# infinite loop
while True:
    imgs = []
    for s in stream:
        (grabbed, frame) = s.read()
        # check if frame empty
        if not grabbed:
            print('opencv is buggy')
            break
        frame = cv2.resize(frame, (960, 540))
        imgs.append(frame)

    # (grabbed, frame) = stream.read()
    # read frames

    # frame = cv2.resize(frame, (960, 540))
    # imgs = [frame]
    results = model(imgs, size=640)  # includes NMS

    results.print()
    results.render()
    # for img in results.imgs:
    #     cv2.imshow("Output Frame", results.imgs[0])
    imgs_show = np.hstack(results.imgs)
    cv2.imshow("Output Frame", imgs_show)
    # cv2.imshow("Output Frame", frame)

    # Show output window

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

cv2.destroyAllWindows()
# close output window

stream.release()
