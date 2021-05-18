class fence_result:
    # 建構式
    def __init__(self, alert, image,):
        self.alert = alert
        self.image = image


def fence_algorithm(inside, last_image, this_image):
    result = fence_result(True, b'')
    return result
