import cv2

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/Snapchat/5.png', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(x, w):
    maskWidth = w - x + 100
    origMaskHeight, origMaskWidth = raw_image.shape[:2]
    maskHeight = maskWidth * origMaskHeight / origMaskWidth

    return maskWidth, maskHeight


def getFaceDimensions(shape):
    x = shape.part(1).x
    w = shape.part(15).x
    y = shape.part(20).y
    h = shape.part(8).y

    return x, w, y, h


def getRegionOfInterest(shape):
    x, w, y, h= getFaceDimensions(shape)

    # # The mask should be proportionate to size of face
    maskWidth, maskHeight = resizeMask(x, w)

    # Getting dimensions of region of interest
    x1 = shape.part(29).x - (maskWidth / 2)
    x2 = shape.part(29).x + (maskWidth / 2)
    y1 = shape.part(29).y - (maskHeight / 2) - 200
    y2 = shape.part(29).y + (maskHeight / 2) - 200

    return x1, x2, y1, y2
