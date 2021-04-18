# !/usr/bin/python
# coding:utf-8
from flask import jsonify


class selectionSort():
    # 建構式
    def __init__(self, data):
        self.data = data

    def selectionSortResponse(self):
        return jsonify(self.data)

    @classmethod
    def selectionSortCls(cls, data):
        return cls(data)
