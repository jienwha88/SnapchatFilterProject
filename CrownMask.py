


import cv2


def loadImage():
    global image
    image = cv2.imread('images/Snapchat/5.png', cv2.IMREAD_UNCHANGED)
    # image = cv2.imread('images/Png/7.png', cv2.IMREAD_UNCHANGED)


    # Create the mask for the mustache
    orig_mask = image[:, :, 3]

    # Create the inverted mask for the mustache
    orig_mask_inv = cv2.bitwise_not(orig_mask)

    # Convert mustache image to BGR
    # and save the original image size (used later when re-sizing the image)
    image = image[:, :, 0:3]

    return image, orig_mask, orig_mask_inv


def resizeMask(x, w, y, h):
    # The mustache should be three times the width of the nose
    maskWidth = w - x + 100
    origMaskHeight, origMaskWidth = image.shape[:2]
    maskHeight = maskWidth * origMaskHeight / origMaskWidth

    # return origMaskWidth - 100, origMaskHeight - 100

    # return origMaskWidth, origMaskHeight
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
    maskWidth, maskHeight = resizeMask(x, w, y, h)
    # Getting dimensions of region of interest
    x1 = shape.part(29).x - (maskWidth / 2)
    x2 = shape.part(29).x + (maskWidth / 2)
    y1 = shape.part(29).y - (maskHeight / 2) - 200
    y2 = shape.part(29).y + (maskHeight / 2) - 200
    return x1, x2, y1, y2
