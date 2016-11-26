import cv2  # OpenCV Library

# -----------------------------------------------------------------------------
#       Load and configure Haar Cascade Classifiers
# -----------------------------------------------------------------------------

# location of OpenCV Haar Cascade Classifiers:
baseCascadePath = "haarcascade/"

# xml files describing our haar cascade classifiers
faceCascadeFilePath = baseCascadePath + "haarcascade_frontalface_default.xml"
noseCascadeFilePath = baseCascadePath + "haarcascade_mcs_nose.xml"
eyeCascadeFilePath = baseCascadePath + "haarcascade_eye.xml"
mouthCascadeFilePath = baseCascadePath + "haarcascade_mouth.xml"

# build our cv2 Cascade Classifiers
faceCascade = cv2.CascadeClassifier(faceCascadeFilePath)
noseCascade = cv2.CascadeClassifier(noseCascadeFilePath)
eyeCascade = cv2.CascadeClassifier(eyeCascadeFilePath)
mouthCascade = cv2.CascadeClassifier(mouthCascadeFilePath)

# -----------------------------------------------------------------------------
#       Load and configure mustache (.png with alpha transparency)
# -----------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------
#       Main program loop
# -----------------------------------------------------------------------------

# collect video input from first webcam on system
video_capture = cv2.VideoCapture(0)

while True:
    # Capture video feed
    ret, frame = video_capture.read()

    # Create greyscale image from the video feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in input video stream
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Iterate over each face found
    for (x, y, w, h) in faces:
        # Un-comment the next line for debug (draw box around all faces)
        face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect a nose within the region bounded by each face (the ROI)
        # nose = noseCascade.detectMultiScale(roi_gray)
        nose = noseCascade.detectMultiScale(roi_gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30,30))



        for (nx, ny, nw, nh) in nose:
            print 'face y: ', y, 'nose ny: ', ny
            print 'face h: ', h, 'nose nh: ', nh
            if (ny >= (y + h) / 2) or ny >= y :
                print 'not a valid nose'
                continue

            # Un-comment the next line for debug (draw box around the nose)
            cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(255,0,0),2)



            # The mustache should be three times the width of the nose
            mustacheWidth = 3 * nw
            mustacheHeight = mustacheWidth * origMustacheHeight / origMustacheWidth

            # Center the mustache on the bottom of the nose
            x1 = nx - (mustacheWidth / 4)
            x2 = nx + nw + (mustacheWidth / 4)
            y1 = ny + nh - (mustacheHeight / 2)
            y2 = ny + nh + (mustacheHeight / 2)

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

            # roi_bg contains the original image only where the mustache is not
            # in the region that is the size of the mustache.
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

            # roi_fg contains the image of the mustache only where the mustache is
            roi_fg = cv2.bitwise_and(mustache, mustache, mask=mask)

            # join the roi_bg and roi_fg
            dst = cv2.add(roi_bg, roi_fg)

            # place the joined image, saved to dst back over the original image
            roi_color[y1:y2, x1:x2] = dst

            break


    # Display the resulting frame
    cv2.imshow('Video', frame)

    # press any key to exit
    if cv2.waitKey(1) == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()