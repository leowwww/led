from cv2 import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
import svm_predict 
import time
import Needl
from digital_detection import ExtractNum 
import pandas as pd


#fps = video.get(cv2.cv.CV_CAP_PROP_FPS)#每秒的帧数

def leo(video_addr):
    videoCapture = cv2.VideoCapture(video_addr)
    success, frame = videoCapture.read()
    i = 0
    timef = videoCapture.get(cv2.CAP_PROP_FPS)
    j = 0
    up_content= []
    lower_content = []
    while success:
        i = i + 1
        if (i % timef == 0):
            image = frame
            #将图片进行识别返回识别的数字
            up , lower = ExtractNum(image)
            up_content.append(up)
            lower_content.append(lower)
        success , frame = videoCapture.read()
    return up_content , lower_content
def save_date(data1 , data2 , filename = None):
    df = pd.DataFrame({'上屏幕':data1 ,'下屏幕':data2})
    if filename == None:
        df.to_excel('c:/1.xlsx')
    else:
        df.to_excel(filename)

if __name__ == "__main__":
    up , lower = leo()