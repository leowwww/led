# !usr/bin/python
# -*- coding:utf-8 -*-

"""A load svm train function"""

__author__ = "huzhenhong-2019-12-25"

import os
import numpy as np
import cv2 as cv
#import base_function as bf

svm = cv.ml.SVM_load('svm_data.dat')

# img = cv.imread('template/3.jpg', cv.IMREAD_GRAYSCALE)
def  predict(img):
    #img = cv.imread(img_file, cv.IMREAD_GRAYSCALE)(128*64)
    img = np.array(img, dtype='float32').reshape(-1, 128*64)
    _, y_pred = svm.predict(img)
    print(int(y_pred[0][0]))
    return int(y_pred[0][0])