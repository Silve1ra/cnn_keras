#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

    Abstract class for classifiers.

    Name: classifier.py
    Author: Gabriel Kirsten Menezes (gabriel.kirsten@hotmail.com)

"""

import numpy
import cv2
import argparse

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Flatten, Dense
import sys

img_width, img_height = 28, 28

#outputClasses = ["FolhaSaudavel", "Gramineas", "Mildio", "Solo",
#                 "FerrugemAsiatica",  "FolhasLargas", "Mancha_Alvo", "Palha"]


def get_args():
    """Read the arguments of program."""
    ap = argparse.ArgumentParser()

    ap.add_argument("-cl", "--classes", required=True, help="Classes names",
                    default=None, type=str)

    ap.add_argument("-i", "--inputimage", required=True, help="Input image " +
                    "for the classifier", default=None, type=str)

    return vars(ap.parse_args())


def create_model():
    """Create the model"""
    model = Sequential()

    model.add(Convolution2D(16, (5, 5), activation='relu',
              input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(2, 2))

    model.add(Convolution2D(32, (5, 5), activation='relu'))
    model.add(MaxPooling2D(2, 2))

    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))

    model.add(Dense(8, activation='softmax'))

    model.summary()

    return model


# read args
get_args()

# load classes
outputClasses = args["classes"].split()

# load image
img = cv2.imread(args["inputimage"])
img = cv2.resize(img, (img_width, img_height))

model = create_model()

model.load_weights('./weith_neuralnet.h5')

arr = numpy.array(img).reshape((img_width, img_height, 3))
arr = numpy.expand_dims(arr, axis=0)
prediction = model.predict(arr)[0]

# name of the best class
bestclass = ''

bestconf = -1

for n in [0, 1]:
    if (prediction[n] > bestconf):
        bestclass = str(n)
        bestconf = prediction[n]

print 'Class: ' + outputClasses[int(bestclass)] + '(' + bestclass + ')'
+ ' with ' + str(bestconf * 100) + '% confidence.'