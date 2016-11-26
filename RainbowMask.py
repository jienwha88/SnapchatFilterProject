
import cv2


def loadImage():
    global image
    # Load our overlay image: mustache.png
    # image = cv2.imread('images/mustache.png', -1)
    image = cv2.imread('images/Snapchat/4.png', cv2.IMREAD_UNCHANGED)

    # print imgMustache

    # Create the mask for the mustache
    orig_mask = image[:, :, 3]

    # Create the inverted mask for the mustache
    orig_mask_inv = cv2.bitwise_not(orig_mask)

    # Convert mustache image to BGR
    # and save the original image size (used later when re-sizing the image)
    image = image[:, :, 0:3]

    return image, orig_mask, orig_mask_inv


def resizeMask(nx, nw):
    # The mustache should be three times the width of the nose
    maskWidth = 3 * (nw - nx)
    origMaskHeight, origMaskWidth = image.shape[:2]
    maskHeight = maskWidth * origMaskHeight / origMaskWidth
    return maskWidth, maskHeight


def getWidthOfNose(shape):
    nx = shape.part(60).x
    nw = shape.part(54).x
    return nx, nw

def getRegionOfInterest(shape):
    # Getting dimensions of nose
    nx, nw = getWidthOfNose(shape)
    # # The mask should be proportionate to size of face
    maskWidth, maskHeight = resizeMask(nx, nw)
    # Getting dimensions of region of interest
    x1 = shape.part(52).x - (maskWidth / 2)
    x2 = shape.part(52).x + (maskWidth / 2)
    y1 = shape.part(52).y - (maskHeight / 2) + 100
    y2 = shape.part(52).y + (maskHeight / 2) + 100
    return x1, x2, y1, y2
