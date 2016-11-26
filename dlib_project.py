# Import required modules
import cv2
import dlib

import MustacheMask as mm

def addMaskToFrame():
    # roi_bg contains the original image only where the mustache is not
    # in the region that is the size of the mustache.
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    # roi_fg contains the image of the mustache only where the mustache is
    roi_fg = cv2.bitwise_and(mustache, mustache, mask=mask)

    # join the roi_bg and roi_fg
    dst = cv2.add(roi_bg, roi_fg)

    # place the joined image, saved to dst back over the original image
    roi_color[y1:y2, x1:x2] = dst


# Load our overlay image: mustache.png
imgMustache = cv2.imread('images/mustache.png', -1)
# imgMustache = cv2.imread('images/Snapchat/1.png', cv2.IMREAD_UNCHANGED)

# print imgMustache

# Create the mask for the mustache
orig_mask = imgMustache[:, :, 3]

# Create the inverted mask for the mustache
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert mustache image to BGR
# and save the original image size (used later when re-sizing the image)
imgMustache = imgMustache[:, :, 0:3]
origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]


# Set up some required objects
video_capture = cv2.VideoCapture(0)  # Webcam object
detector = dlib.get_frontal_face_detector()  # Face detector
predictor = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")  # Landmark identifier. Set the filename to whatever you named the downloaded file



while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray)

    detections = detector(clahe_image, 1)  # Detect the faces in the image

    for k, d in enumerate(detections):  # For each detected face

        shape = predictor(clahe_image, d)  # Get coordinates

        # Uncomment for debugging
        # for i in range(1, 68):  # There are 68 landmark points on each face
        #     cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0, 0, 255),
        #                thickness=2)  # For each point, draw a red circle with thickness2 on the original frame


        # cv2.circle(frame, (shape.part(33).x, shape.part(33).y), 20, (0, 0, 255),
        #            thickness=2)
        #
        # cv2.circle(frame, (shape.part(2).x, shape.part(2).y), 20, (0, 0, 255),
        #            thickness=2)
        #

        # cv2.circle(frame, (shape.part(30).x, shape.part(30).y), 20, (0, 0, 255),
        #            thickness=2)

        # mm.getMask(frame, shape)

        #Getting dimensions of face
        y = shape.part(20).y
        h = shape.part(9).y
        x = shape.part(2).x
        w = shape.part(16).x

        #Getting region of interest of face
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        #Getting dimensions of nose
        nx = shape.part(30).x - x
        ny = shape.part(33).y - y
        nw = shape.part(35).x - x
        nh = shape.part(28).y - y

        # The mustache should be three times the width of the nose
        mustacheWidth = 6 * (nw-nx)
        mustacheHeight = mustacheWidth * origMustacheHeight / origMustacheWidth



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

        # Re-size the original image and the masks to the mustache sizes
        # calcualted above
        mustache = cv2.resize(imgMustache, (mustacheWidth, mustacheHeight), interpolation=cv2.INTER_AREA)
        mask = cv2.resize(orig_mask, (mustacheWidth, mustacheHeight), interpolation=cv2.INTER_AREA)
        mask_inv = cv2.resize(orig_mask_inv, (mustacheWidth, mustacheHeight), interpolation=cv2.INTER_AREA)

        # take ROI for mustache from background equal to size of mustache image
        roi = roi_color[y1:y2, x1:x2]

        try:
            addMaskToFrame()
            # # roi_bg contains the original image only where the mustache is not
            # # in the region that is the size of the mustache.
            # roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            #
            # # roi_fg contains the image of the mustache only where the mustache is
            # roi_fg = cv2.bitwise_and(mustache, mustache, mask=mask)
            #
            # # join the roi_bg and roi_fg
            # dst = cv2.add(roi_bg, roi_fg)
            #
            # # place the joined image, saved to dst back over the original image
            # roi_color[y1:y2, x1:x2] = dst

        except:
            # In case of exceptions, just skip the frame and do not display mask
            print 'Invalid values, do not add mask'
            continue


    cv2.imshow("image", frame)  # Display the frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit program when the user presses 'q'
        break