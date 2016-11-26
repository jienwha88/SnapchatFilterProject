# Import required modules
import cv2
import dlib

import MustacheMask
import DogMask
import RainbowMask
import CrownMask

def addMaskToFrame():
    # roi_bg contains the original image only where the mustache is not
    # in the region that is the size of the mustache.
    roi_bg = cv2.bitwise_and(roi, roi, mask=resized_mask_inv)

    # roi_fg contains the image of the mustache only where the mustache is
    roi_fg = cv2.bitwise_and(resized_image, resized_image, mask=resized_mask)

    # join the roi_bg and roi_fg
    dst = cv2.add(roi_bg, roi_fg)

    # place the joined image, saved to dst back over the original image
    # roi_color[y1:y2, x1:x2] = dst
    frame[y1:y2, x1:x2] = dst


abstractMask = MustacheMask
# abstractMask = DogMask
# abstractMask = RainbowMask
# abstractMask = CrownMask


image, orig_mask, orig_mask_inv = abstractMask.loadImage()

# Set up some required objects
video_capture = cv2.VideoCapture(0)  # Webcam object
detector = dlib.get_frontal_face_detector()  # Face detector
predictor = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")  # Landmark identifier. Set the filename to whatever you named the downloaded file


while True:
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)
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
        # cv2.circle(frame, (shape.part(31).x, shape.part(31).y), 20, (0, 0, 255),
        #            thickness=2)
        # cv2.circle(frame, (shape.part(35).x, shape.part(35).y), 20, (0, 0, 255),
        #            thickness=2)

        # mm.getMask(frame, shape)


        # cv2.circle(frame, (shape.part(52).x, shape.part(52).y), 20, (0, 0, 255),
        #            thickness=2)
        # cv2.circle(frame, (shape.part(54).x, shape.part(54).y), 20, (0, 0, 255),
        #            thickness=2)



        x1, x2, y1, y2 = abstractMask.getRegionOfInterest(shape)

        # Re-calculate the width and height of the mustache image
        roi_width = x2 - x1
        roi_height = y2 - y1

        # Re-size the original image and the masks to the mustache sizes calculated above
        resized_image = cv2.resize(image, (roi_width, roi_height), interpolation=cv2.INTER_AREA)
        resized_mask = cv2.resize(orig_mask, (roi_width, roi_height), interpolation=cv2.INTER_AREA)
        resized_mask_inv = cv2.resize(orig_mask_inv, (roi_width, roi_height), interpolation=cv2.INTER_AREA)

        # take ROI for mustache from background equal to size of mustache image
        roi = frame[y1:y2, x1:x2]

        try:
            addMaskToFrame()
        except:
            # In case of exceptions, just skip the frame and do not display mask
            print 'Invalid values, do not add mask'
            continue


    cv2.imshow("image", frame)  # Display the frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit program when the user presses 'q'
        break