import os
import sys

from glob import glob


import numpy as np
import cv2
import project as pr

def readImages(image_dir):
    extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg',
                  'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']


    search_paths = [os.path.join(image_dir, '*.' + ext) for ext in extensions]
    image_files = sorted(reduce(list.__add__, map(glob, search_paths)))
    images = [cv2.imread(f, cv2.IMREAD_UNCHANGED | cv2.IMREAD_COLOR)
              for f in image_files]

    return images


if __name__ == "__main__":
    print "Reading images."
    # images = readImages("images")
    image = cv2.imread("images/sundial_with_bros.jpg")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    pr.detectFaces(image, gray)

