# !/usr/bin/python
# coding:utf-8
from flask import jsonify


class quickSort():
    # 建構式
    def __init__(self, data):
        self.data = data

    def quickSortResponse(self):
        return jsonify(self.data)

    @classmethod
    def quickSortCls(cls, data):
        return cls(data)
