import cv2
import Constants as const

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/crown.png', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(x, w):
    maskWidth = int((w - x) * 1.5)
    origMaskHeight, origMaskWidth = raw_image.shape[:2]
    maskHeight = maskWidth * origMaskHeight / origMaskWidth

    return maskWidth, maskHeight


def getFaceDimensions(shape):
    x = shape.part(const.CHEEK_LEFT).x
    w = shape.part(const.CHEEK_RIGHT).x
    y = shape.part(const.EYEBROW_TOP).y
    h = shape.part(const.CHIN).y

    return x, w, y, h


def getRegionOfInterest(shape):
    x, w, y, h= getFaceDimensions(shape)

    # # The mask should be proportionate to size of face
    maskWidth, maskHeight = resizeMask(x, w)

    distance = int((shape.part(const.CHIN).y - shape.part(const.NOSE_TOP).y) * 1.5)

    # Getting dimensions of region of interest
    x1 = shape.part(const.NOSE_TOP).x - (maskWidth / 2)
    x2 = shape.part(const.NOSE_TOP).x + (maskWidth / 2)
    y1 = shape.part(const.NOSE_TOP).y - (maskHeight / 2) - distance
    y2 = shape.part(const.NOSE_TOP).y + (maskHeight / 2) - distance

    return x1, x2, y1, y2
