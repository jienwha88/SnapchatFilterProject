import cv2

def loadImage():
    global raw_image
    raw_image = cv2.imread('images/mustache.png', cv2.IMREAD_UNCHANGED)

    return raw_image


def resizeMask(nx, nw):
    mask_width = 3 * (nw - nx)
    orig_mask_height, orig_mask_width = raw_image.shape[:2]
    mask_height = mask_width * orig_mask_height / orig_mask_width

    return mask_width, mask_height


def getWidthOfNose(shape):
    nx = shape.part(31).x
    nw = shape.part(35).x

    return nx, nw


def getRegionOfInterest(shape):
    nx, nw = getWidthOfNose(shape)

    # The mask should be proportionate to size of nose
    mask_width, mask_height = resizeMask(nx, nw)

    # Getting dimensions of region of interest
    x1 = shape.part(33).x - (mask_width / 2)
    x2 = shape.part(33).x + (mask_width / 2)
    y1 = shape.part(33).y - (mask_height / 2) + 15
    y2 = shape.part(33).y + (mask_height / 2) + 15

    return x1, x2, y1, y2
