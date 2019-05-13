#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import numpy
import imageio
import math
from picamera import PiCamera
from io import BytesIO
from time import sleep

target_path = "Black&WhitePot.png"
threshold = 80
camera = PiCamera()
stream = BytesIO()

def binarize_array(numpy_array, threshold=200):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

def sum_colour_of_square(numpy_array):
    sum_four_by_four_square = 0
    for y in range(len(numpy_array)):
        for x in range(len(numpy_array[0])):
            sum_four_by_four_square += numpy_array[y][x]
    return sum_four_by_four_square

def clean_image(numpy_array, threshold=200):
    test_array = numpy.zeros(shape=(426,320))
    for i in range(math.floor(len(numpy_array)/4)):
        for j in range(math.floor(len(numpy_array[0])/4)):
            sum_four_by_four_square = sum_colour_of_square(numpy_array[i:i+3, j:j+3])
            avg_colour = sum_four_by_four_square/16
            if numpy_array[i][j] > threshold: #avg_colour
                test_array[i][j] = 255
            else:
                test_array[i][j] = 0
    return test_array

def make_black_and_white_stripe(numpy_array, threshold=200):
    height_of_original_image = numpy_array.shape[0]
    width_of_original_image = numpy_array.shape[1]
    black_and_white_stripe = numpy.zeros((height_of_original_image, 1))
    for i in range(len(numpy_array)):
        average_colour_of_horizonal = sum(numpy_array[i])/width_of_original_image 
        if average_colour_of_horizonal > 255/2:
            black_and_white_stripe[i][0] = 255
        else:
            black_and_white_stripe[i][0] = 0
        #for j in range(len()):
        #    if numpy_array[i][j] > threshold:
        #        numpy_array[i][j] = 255
        #    else:
        #        numpy_array[i][j] = 0
    return black_and_white_stripe

camera.resolution = (640, 360)
camera.framerate = 24
#camera.color_effects = (128,128) # turn camera to black and white
# sleep(2)
camera.capture(stream, format='png')
stream.seek(0)
image = Image.open(stream)
image = image.convert('L')
image = numpy.array(image)
imageio.imwrite("Original.png", image)

image_black_and_white = binarize_array(image, threshold)
imageio.imwrite("Black&WhitePot.png", image_black_and_white)

#image_clean = clean_image(image, threshold)
#imageio.imwrite("CleanedImage.png", image_clean)

black_and_white_stripe = make_black_and_white_stripe(image)
imageio.imwrite("Black&WhiteStripe.png", black_and_white_stripe)
