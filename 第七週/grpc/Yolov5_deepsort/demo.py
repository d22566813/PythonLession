from AIDetector_pytorch import Detector
import imutils
import cv2
import pafy


def main():

    func_status = {}
    func_status['headpose'] = None

    name = 'demo'

    det = Detector(['person'])
    video = pafy.new(
        "https://www.youtube.com/watch?v=wCcMcaiRbhM&list=PL-Ni-1OtjEdLtQRpD-6r9AsD3P_6MLpgv&index=66")
    play = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(play.url)

    # cap = cv2.VideoCapture('./MOT16-03.mp4')
    fps = int(cap.get(5))
    print('fps:', fps)
    t = int(1000/fps)

    size = None
    videoWriter = None

    while True:

        # try:
        (_, im) = cap.read()
        if im is None:
            break
        im = cv2.resize(im, (960, 540))

        result = det.feedCap(im, func_status)
        result = result['frame']
        result = imutils.resize(result, height=500)
        # if videoWriter is None:
        #     fourcc = cv2.VideoWriter_fourcc(
        #         'm', 'p', '4', 'v')  # opencv3.0
        #     videoWriter = cv2.VideoWriter(
        #         'result.mp4', fourcc, fps, (result.shape[1], result.shape[0]))

        # videoWriter.write(result)
        cv2.imshow(name, result)
        cv2.waitKey(t)

        # if cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) < 1:
        #     # 点x退出
        #     break
        # except Exception as e:
        #     print(e)
        #     break

    # cap.release()
    # # videoWriter.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':

    main()
