# !/usr/bin/python
# coding:utf-8

from flask import Flask, jsonify, request
from config import DevConfig
from Sort.heapSort import heapSort
from Sort.insertionSort import insertionSort
from Sort.mergeSort import mergeSort
from Sort.quickSort import quickSort
from Sort.selectionSort import selectionSort

# 初始化 Flask 類別成為 instance
app = Flask(__name__)
app.config.from_object(DevConfig)

# 路由和處理函式配對


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/sort/quickSort', methods=['POST'])
def quickSortPage():
    data = request.get_json()
    quick_sort = quickSort(data)
    return quick_sort.quickSortResponse()
    # 另一種寫法
    # quick_sort = quickSort.quickSortCls(data)
    # return quick_sort.quickSortResponse()


@app.route('/sort/mergeSort', methods=['POST'])
def mergeSortPage():
    data = request.get_json()
    merge_sort = mergeSort(data)
    return merge_sort.mergeSortResponse()
    # 另一種寫法
    # merge_sort = mergeSort.mergeSortCls(data)
    # return merge_sort.mergeSortResponse()


@app.route('/sort/insertionSort', methods=['POST'])
def insertionSortPage():
    data = request.get_json()
    insertion_sort = insertionSort(data)
    return insertion_sort.insertionSortResponse()
    # 另一種寫法
    # insertion_sort = insertionSort.insertionSortCls(data)
    # return insertion_sort.insertionSortResponse()


@app.route('/sort/heapSort', methods=['POST'])
def heapSortPage():
    data = request.get_json()
    heap_sort = heapSort(data)
    heap_sort.heapSortAlgorithm()
    return heap_sort.heapSortResponse()
    # 另一種寫法
    # heap_sort = heapSort.heapSortCls(data)
    # return heap_sort.heapSortResponse()


@app.route('/sort/selectionSort', methods=['POST'])
def selectionSortPage():
    data = request.get_json()
    selection_sort = selectionSort(data)
    return selection_sort.selectionSortResponse()
    # 另一種寫法
    # selection_sort = selectionSort.selectionSortCls(data)
    # rreturn selection_sort.selectionSortResponse()


# 判斷自己執行非被當做引入的模組，因為 __name__ 這變數若被當做模組引入使用就不會是 __main__
if __name__ == '__main__':
    app.run()
