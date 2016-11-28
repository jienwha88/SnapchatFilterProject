import cv2
import Constants as const

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/vendetta.png', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(x, w, y, h):
    mask_width = w - x
    mask_height = int((h - y) * 1.5)

    return mask_width, mask_height


def getFaceDimensions(shape):
    x = shape.part(const.CHEEK_LEFT).x
    w = shape.part(const.CHEEK_RIGHT).x
    y = shape.part(const.EYEBROW_TOP).y
    h = shape.part(const.CHIN).y

    return x, w, y, h


def getRegionOfInterest(shape):
    x, w, y, h = getFaceDimensions(shape)
    # The mask should be proportionate to size of face

    mask_width, mask_height = resizeMask(x, w, y, h)
    # Getting dimensions of region of interest
    x1 = shape.part(const.NOSE_TOP).x - (mask_width / 2)
    x2 = shape.part(const.NOSE_TOP).x + (mask_width / 2)
    y1 = shape.part(const.NOSE_TOP).y - (mask_height / 2)
    y2 = shape.part(const.NOSE_TOP).y + (mask_height / 2)

    return x1, x2, y1, y2
