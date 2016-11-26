import cv2
import dlib
import sys

import MustacheMask
import DogMask
import RainbowMask
import CrownMask

# Prompts user to select a mask
def selectMask():
    print "Select image for mask: "
    print "\t1) Mustache"
    print "\t2) Dog"
    print "\t3) Rainbow"
    print "\t4) Crown"
    print "\tq to exit"
    while(True):
        input = raw_input("Selection: ")
        if input == '1':
            return MustacheMask
        elif input == '2':
            return DogMask
        elif input == '3':
            return RainbowMask
        elif input == '4':
            return CrownMask
        elif input == 'q':
            sys.exit(0)
        else:
            print "Please enter a valid choice"

# Adds the mask to the frame
def addMaskToFrame():
    # Keep background the same by using the mask inverse
    background = cv2.bitwise_and(roi, roi, mask=resized_mask_inv)

    # Mask out everything but the image
    masked_image = cv2.bitwise_and(resized_image, resized_image, mask=resized_mask)

    # Add image to background
    merged_roi = cv2.add(background, masked_image)

    # Replace the frame with the merged region of interest
    frame[y1:y2, x1:x2] = merged_roi


# Setup video capture via webcam
video_capture = cv2.VideoCapture(0)

# Use the dlib frontal face detector
dlib_detector = dlib.get_frontal_face_detector()

# Face Detector file, downloaded from: "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
dlib_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# Prompts user to enter mask
abstractMask = selectMask()

# Loads image based on mask chosen
raw_image = abstractMask.loadImage()

# Creates the mask
orig_mask = raw_image[:, :, 3]

# Creates the mask inverse
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Converting image into BGR
image = raw_image[:, :, 0:3]

while True:
    # Start capturing frames
    retval, frame = video_capture.read()

    # Mirror Frame
    frame = cv2.flip(frame, 1)

    # Gray scale used for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Creating Contrast Limited Adaptive Histogram Equalization for improved face recognition (equal lighting)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray_frame)

    # Use dlib detector to detect faces
    detections = dlib_detector(clahe_image, 1)

    for k, d in enumerate(detections):
        # Get coordinates of key facial features
        key_facial_features = dlib_predictor(clahe_image, d)

        # Uncomment for debugging
        # for i in range(1, 68):  # There are 68 landmark points on each face
        #     cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0, 0, 255),
        #                thickness=2)  # For each point, draw a red circle with thickness2 on the original frame


        # Get coordinates of region of interest
        # Region of Interest (roi) is the region that includes the mask and background
        x1, x2, y1, y2 = abstractMask.getRegionOfInterest(key_facial_features)

        # Get shape or ROI
        roi_width = x2 - x1
        roi_height = y2 - y1

        # Resizing the images and mask based on ROI
        resized_image = cv2.resize(image, (roi_width, roi_height), interpolation=cv2.INTER_AREA)
        resized_mask = cv2.resize(orig_mask, (roi_width, roi_height), interpolation=cv2.INTER_AREA)
        resized_mask_inv = cv2.resize(orig_mask_inv, (roi_width, roi_height), interpolation=cv2.INTER_AREA)

        # Create ROI
        roi = frame[y1:y2, x1:x2]

        try:
            # Combining the mask to the frame
            addMaskToFrame()
        except:
            # In case of exceptions, just skip the frame and do not display mask
            print 'Invalid values, do not add mask'
            continue

    # Displays the new frame
    cv2.imshow("image", frame)

    # Exit program when the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.release()
        cv2.destroyAllWindows()
        break
