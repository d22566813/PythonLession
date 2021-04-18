list = {'A', 'B', 'C'}


def Algorithm(top, bottom, src='A', target='C'):
    if top == bottom:  # 單純移動一個盤子
        print('%d move from %s to %s' % (top, src, target))
    else:  # 移動兩個盤子
        tmp = (list - {src, target}).pop()  # 暫存柱子
        # 遞迴
        Algorithm(1, bottom - 1, src, tmp)      # 先把倒數第二個盤子放到暫存柱子
        Algorithm(bottom, bottom, src, target)  # 移动最底下的盘子
        Algorithm(1, bottom - 1, tmp, target)   # 再把倒数第二個盤子放到目標柱子


numberInput = input("How many plates?(1-10)\n")
while not numberInput.isdigit():
    numberInput = input("How many plates?(1-10)\n")

number = int(numberInput)
if number >= 1 and number <= 10:
    Algorithm(1, number)
