import cv2
import Constants as const

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/rainbow.png', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(wx, ww):
    maskWidth = 3 * (ww - wx)
    origMaskHeight, origMaskWidth = raw_image.shape[:2]
    maskHeight = maskWidth * origMaskHeight / origMaskWidth
    return maskWidth, maskHeight


def getWidthOfMouth(shape):
    wx = shape.part(const.MOUTH_LEFT).x
    ww = shape.part(const.MOUTH_RIGHT).x
    return wx, ww


def getRegionOfInterest(shape):
    wx, ww = getWidthOfMouth(shape)

    # # The mask should be proportionate to size of mouth
    maskWidth, maskHeight = resizeMask(wx, ww)

    distance = int((shape.part(const.MOUTH_TOP).y - shape.part(const.NOSE_TOP).y))

    # Getting dimensions of region of interest
    x1 = shape.part(const.MOUTH_TOP).x - (maskWidth / 2)
    x2 = shape.part(const.MOUTH_TOP).x + (maskWidth / 2)
    y1 = shape.part(const.MOUTH_TOP).y - (maskHeight / 2) + distance
    y2 = shape.part(const.MOUTH_TOP).y + (maskHeight / 2) + distance

    return x1, x2, y1, y2
