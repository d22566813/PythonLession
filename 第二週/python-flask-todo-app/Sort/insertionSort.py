# !/usr/bin/python
# coding:utf-8
from flask import jsonify


class insertionSort():
    # 建構式
    def __init__(self, data):
        self.data = data

    def insertionSortResponse(self):
        return jsonify(self.data)

    @classmethod
    def insertionSortCls(cls, data):
        return cls(data)
