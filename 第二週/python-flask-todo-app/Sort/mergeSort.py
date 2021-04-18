# !/usr/bin/python
# coding:utf-8
from flask import jsonify


class mergeSort():
    # 建構式
    def __init__(self, data):
        self.data = data

    def mergeSortResponse(self):
        return jsonify(self.data)

    @classmethod
    def mergeSortCls(cls, data):
        return cls(data)
