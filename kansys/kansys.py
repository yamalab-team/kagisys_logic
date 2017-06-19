import cv2


def take_picture():
    '''写真を取ってファイルの保存'''
    # カメラデバイスを取得
    camera = cv2.VideoCapture(0)
    # readで画像をキャプチャ、imgにRGBのデータが入ってくる
    r, img = camera.read()
    # 保存
    cv2.imwrite('photo.jpg', img)
