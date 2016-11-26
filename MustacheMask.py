
import cv2


class MustascheMask:
    # Load our overlay image: mustache.png
    # imgMustache = cv2.imread('images/mustache.png', -1)
    imgMustache = cv2.imread('images/Snapchat/1.png', cv2.IMREAD_UNCHANGED)

    # print imgMustache

    # Create the mask for the mustache
    orig_mask = imgMustache[:, :, 3]

    # Create the inverted mask for the mustache
    orig_mask_inv = cv2.bitwise_not(orig_mask)

    # Convert mustache image to BGR
    # and save the original image size (used later when re-sizing the image)
    imgMustache = imgMustache[:, :, 0:3]
    origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]



def getMask(frame, shape):
    m = MustascheMask()
    cv2.circle(frame, (shape.part(30).x, shape.part(30).y), 20, (0, 0, 255),
               thickness=2)

    imgMustache = m.imgMustache[:, :, 0:3]
    origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]

    y = shape.part(20).y
    h = shape.part(9).y
    x = shape.part(2).x
    w = shape.part(16).x



    # nx = shape.part(34).x - x
    # ny = shape.part(34).y - y
    # nw = shape.part(31).x - shape.part(36).x
    # nh = shape.part(34).y - shape.part(28).y

    nx = shape.part(30).x - x
    ny = shape.part(33).y - y
    nw = shape.part(35).x - x
    nh = shape.part(28).y - y

    # The mustache should be three times the width of the nose
    mustacheWidth = 6 * (nw - nx)
    mustacheHeight = mustacheWidth * origMustacheHeight / origMustacheWidth

    # Center the mustache on the bottom of the nose
    # x1 = nx - (mustacheWidth / 4)
    # x2 = nx + nw + (mustacheWidth / 4)
    # y1 = ny + nh - (mustacheHeight / 2)
    # y2 = ny + nh + (mustacheHeight / 2)

    x1 = shape.part(33).x - (mustacheWidth / 2) - x
    x2 = shape.part(33).x + (mustacheWidth / 2) - x
    y1 = shape.part(33).y - (mustacheHeight / 2) - y + 15
    y2 = shape.part(33).y + (mustacheHeight / 2) - y + 15

    # Center on nose
    # x1 = nx - (mustacheWidth / 4)
    # x2 = nx + nw + (mustacheWidth / 4)
    # y1 = ny + nh - (mustacheHeight / 2)
    # y2 = nh + nh

    # Check for clipping
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 > w:
        x2 = w
    if y2 > h:
        y2 = h

    # Re-calculate the width and height of the mustache image
    mustacheWidth = x2 - x1
    mustacheHeight = y2 - y1


