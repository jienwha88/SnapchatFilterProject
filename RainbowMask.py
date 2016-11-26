import cv2

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/rainbowpng', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(wx, ww):
    maskWidth = 3 * (ww - wx)
    origMaskHeight, origMaskWidth = raw_image.shape[:2]
    maskHeight = maskWidth * origMaskHeight / origMaskWidth
    return maskWidth, maskHeight


def getWidthOfMouth(shape):
    wx = shape.part(60).x
    ww = shape.part(54).x
    return wx, ww


def getRegionOfInterest(shape):
    wx, ww = getWidthOfMouth(shape)

    # # The mask should be proportionate to size of mouth
    maskWidth, maskHeight = resizeMask(wx, ww)

    # Getting dimensions of region of interest
    x1 = shape.part(52).x - (maskWidth / 2)
    x2 = shape.part(52).x + (maskWidth / 2)
    y1 = shape.part(52).y - (maskHeight / 2) + 100
    y2 = shape.part(52).y + (maskHeight / 2) + 100

    return x1, x2, y1, y2
