import cv2

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/dog.png', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(x, w, y, h):
    mask_width = w - x + 100
    mask_height = h - y + 350

    return mask_width, mask_height


def getFaceDimensions(shape):
    x = shape.part(1).x
    w = shape.part(15).x
    y = shape.part(20).y
    h = shape.part(8).y

    return x, w, y, h


def getRegionOfInterest(shape):
    x, w, y, h = getFaceDimensions(shape)
    # The mask should be proportionate to size of face

    mask_width, mask_height = resizeMask(x, w, y, h)
    # Getting dimensions of region of interest
    x1 = shape.part(29).x - (mask_width / 2)
    x2 = shape.part(29).x + (mask_width / 2)
    y1 = shape.part(29).y - (mask_height / 2)
    y2 = shape.part(29).y + (mask_height / 2)

    return x1, x2, y1, y2
