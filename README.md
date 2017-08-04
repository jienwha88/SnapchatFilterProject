# Snapchat Face Filter
## Technology Stack
1) Python  
2) OpenCV  
3) Dlib

##Result!
![Mustache Screenshot](https://github.com/jienwha88/SnapchatFilterProject/blob/master/result-screenshot.png)

Video:
https://drive.google.com/open?id=0B-azLmpma_FjaDJBNU85YUNhWE0

## Setups
1) Make sure you have Python, OpenCV and Dlib installed.  
Dlib can be installed by following the instructions found here: https://github.com/davisking/dlib  
2) Download the trained face shape predictor from:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2  
Add the file to your project folder.

## Running the project
1) Run the Project.py, you can use the command python Project.py  
2) Select the image to use by entering a value between 1 to 5. Press 'q' to quit.  
3) Once an image is selected, the webcam feed will start automatically and a window of the feed will popup immediately. You should be able to see the images added to the frames.   
4) Enjoy the filters! Press 'q' to close the window.

Note: If you are unable to see the images added to the frames, take a step away from the camera. The image mask will only be added if there is enough room for the frame to add the image mask.
