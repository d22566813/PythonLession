#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/18 下午6:02
# @Author : zengwb

import argparse
import os
import time
import platform
import shutil
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized
import pafy
from utils.datasets import LoadStreams, LoadImages, LoadWebcam
from PIL import Image, ImageDraw, ImageFont


class Detector(baseDet):

    def __init__(self):
        super(Detector, self).__init__()
        self.init_model()
        self.build_config()

    def init_model(self):

        self.weights = 'weights/yolov5s.pt'
        self.device = '0' if torch.cuda.is_available() else 'cpu'
        self.device = select_device(self.device)
        model = attempt_load(self.weights, map_location=self.device)
        model.to(self.device).eval()
        model.half()
        # torch.save(model, 'test.pt')
        self.m = model
        self.names = model.module.names if hasattr(
            model, 'module') else model.names

    def preprocess(self, img):

        img0 = img.copy()
        img = letterbox(img, new_shape=self.img_size)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half()  # 半精度
        img /= 255.0  # 图像归一化
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        return img0, img

    def detect(self, im):

        im0, img = self.preprocess(im)

        pred = self.m(img, augment=False)[0]
        pred = pred.float()
        pred = non_max_suppression(pred, self.threshold, 0.4)

        pred_boxes = []
        for det in pred:

            if det is not None and len(det):
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()

                for *x, conf, cls_id in det:
                    lbl = self.names[int(cls_id)]
                    if not lbl in ['person', 'car', 'truck']:
                        continue
                    x1, y1 = int(x[0]), int(x[1])
                    x2, y2 = int(x[2]), int(x[3])
                    pred_boxes.append(
                        (x1, y1, x2, y2, lbl, conf))

        return im, pred_boxes


def set_parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--source', type=str, default='/media/zengwb/PC/Dataset/ReID-dataset/channel1/1.mp4',
    #                     help='source')  # file/folder, 0 for webcam
    # parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
    # parser.add_argument('--img-size', type=int, default=960, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.2, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.5, help='IOU threshold for NMS')

    parser.add_argument('--view-img', default=True, help='display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='save results to *.txt')

    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')
    parser.add_argument('--update', action='store_true',
                        help='update all models')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument("--camera", action="store",
                        dest="cam", type=int, default="-1")
    parser.add_argument('--weights', nargs='+', type=str,
                        default='./weights/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument(
        '--classes', default=[0], type=int, help='filter by class: --class 0, or --class 0 2 3')

    return parser.parse_args()


def bbox_r(width, height, *xyxy):
    """" Calculates the relative bounding box from absolute pixel values. """
    bbox_left = min([xyxy[0].item(), xyxy[2].item()])
    bbox_top = min([xyxy[1].item(), xyxy[3].item()])
    bbox_w = abs(xyxy[0].item() - xyxy[2].item())
    bbox_h = abs(xyxy[1].item() - xyxy[3].item())
    x_c = (bbox_left + bbox_w / 2)
    y_c = (bbox_top + bbox_h / 2)
    w = bbox_w
    h = bbox_h
    return x_c, y_c, w, h


class Person_detect():
    def __init__(self, opt, source):

        # Initialize
        self.device = opt.device if torch.cuda.is_available() else 'cpu'
        self.half = self.device != 'cpu'  # half precision only supported on CUDA
        self.augment = opt.augment
        self.conf_thres = opt.conf_thres
        self.iou_thres = opt.iou_thres
        self.classes = opt.classes
        self.agnostic_nms = opt.agnostic_nms
        self.webcam = opt.cam
        # Load model
        self.model = attempt_load(
            opt.weights, map_location=self.device)  # load FP32 model
        print('111111111111111111111111111111111111111', self.model.stride.max())
        if self.half:
            self.model.half()  # to FP16

        # Get names and colors
        self.names = self.model.module.names if hasattr(
            self.model, 'module') else self.model.names
        self.colors = [[np.random.randint(0, 255) for _ in range(
            3)] for _ in range(len(self.names))]

    def detect(self, path, img, im0s, vid_cap):

        half = self.device != 'cpu'  # half precision only supported on CUDA

        # print('444444444444444444444444444444444')
        # Run inference
        # print('55555555555555555555555555555')
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = self.model(img, augment=self.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes,
                                   agnostic=self.agnostic_nms)

        # Process detections
        bbox_xywh = []
        confs = []
        clas = []
        xy = []
        for i, det in enumerate(pred):  # detections per image
            # if self.webcam:  # batch_size >= 1
            #     p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
            # else:
            #     p, s, im0 = path, '', im0s
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0s.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    img_h, img_w, _ = im0s.shape  # get image shape
                    x_c, y_c, bbox_w, bbox_h = bbox_r(img_w, img_h, *xyxy)
                    obj = [x_c, y_c, bbox_w, bbox_h]
                    # if cls == opt.classes:  # detct classes id
                    if not conf.item() > 0.3:
                        continue
                    bbox_xywh.append(obj)
                    confs.append(conf.item())
                    clas.append(cls.item())
                    xy.append(xyxy)
                    # print('jjjjjjjjjjjjjjjjjjjj', confs)
        return np.array(bbox_xywh), confs, clas, xy


def draw_boxes(img, bbox, cls_conf, offset=(0, 0)):
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        # id = int(identities[i]) if identities is not None else 0
        color = (int(10*256), int(10*256), int(10*256))
        label = '{}{}'.format("conf:", cls_conf)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        cv2.rectangle(
            img, (x1, y1), (x1 + t_size[0] + 3, y1 + t_size[1] + 4), color, -1)
        cv2.putText(img, label, (x1, y1 +
                                 t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
    return img


def put_text_to_cv2_img_with_pil(cv2_img):
    # cv2和PIL中颜色的hex码的储存顺序不同，需转RGB模式
    pil_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    # Image.fromarray()将数组类型转成图片格式，与np.array()相反
    pilimg = Image.fromarray(pil_img)

    # 将图片转成cv2.imshow()可以显示的数组格式
    return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - \
        new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / \
            shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


if __name__ == '__main__':
    person_detect = Person_detect(opt=set_parser(),
                                  source='/media/zengwb/PC/Dataset/ReID-dataset/channel1/1.mp4')
    video = pafy.new(
        "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66")
    play = video.getbest(preftype="mp4")
    stream = cv2.VideoCapture(play.url)

    detect = Detector()
    while True:
        (grabbed, frame) = stream.read()
        frame = np.stack(frame, 0)
        detect.detect(frame)
        cv2.imshow("Output Frame", frame)
        if(cv2.waitKey(10) == 27):
            break

    cv2.waitKey(10)
    # with torch.no_grad():
    #     dataset = LoadWebcam(play.url, img_size=640)
    #     for video_path, img, ori_img, vid_cap in dataset:
    #         bbox_xywh, cls_conf, cls_ids, xy = person_detect.detect(
    #             video_path, img, ori_img, vid_cap)
    #         ori_img = draw_boxes(ori_img, bbox_xywh, cls_conf)
    #         cv2.imshow("Output Frame", put_text_to_cv2_img_with_pil(ori_img))
