# !/usr/bin/python
# coding:utf-8
from flask import jsonify


def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
    print(arr)
    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        heapify(arr, n, largest)


class heapSort:
    # 建構式
    def __init__(self, data):
        self.data = data

    def heapSortResponse(self):
        return jsonify(self.data)

    @classmethod
    def heapSortCls(cls, data):
        return cls(data)

    def heapSortAlgorithm(self):
        old_array = self.data['array']
        n = len(old_array)
        for i in range(n // 2 - 1, -1, -1):
            heapify(old_array, n, i)
        for i in range(n-1, 0, -1):
            old_array[i], old_array[0] = old_array[0], old_array[i]   # swap
            heapify(old_array, i, 0)

        self.data['array'] = old_array
