from cv2 import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
import svm_predict 
import time
import Needl
#显示图片
def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey()
    cv2.destroyAllWindows()
#显示彩色图片
def plt_show0(img):
    b,g,r = cv2.split(img)
    img = cv2.merge([r, g, b])
    plt.imshow(img)
    plt.show()
#显示灰度图片
def plt_show(img):
    plt.imshow(img,cmap='gray')
    plt.show()

#图像去噪转换成opencv的bgr模式
def gray_guss(image):
    image = cv2.GaussianBlur(image,(3,3),0)
    gray_image = cv2.cvtColor(image , cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    return gray_image
# 提取显示屏部分图片
def get_carLicense_img(image):
    gray_image = gray_guss(image)
    Sobel_x = cv2.Sobel(gray_image, cv2.CV_16S, 0, 1)#边缘检测
    absX = cv2.convertScaleAbs(Sobel_x)
    image = absX
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#做二值化的时候先进行图像的灰度化
    ret, image = cv2.threshold(image, 3, 255, cv2.THRESH_OTSU)#图像二值化
    #cv_show('image',image)
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 4))#开闭操作的模板大小形状是 rect 矩阵
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX,iterations = 3)
    #cv_show('open',image)
    kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 20))
    image = cv2.erode(image, kernelX)#腐蚀
    image = cv2.erode(image , kernelY)
    #cv_show('1',image)
    image = cv2.dilate(image, cv2.getStructuringElement(cv2.MORPH_RECT, (75, 4)))#膨胀
    image = cv2.erode(image, cv2.getStructuringElement(cv2.MORPH_RECT, (4, 10)))#腐蚀
    image = cv2.dilate(image, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 29)))#膨胀
    image = cv2.medianBlur(image, 1)
    #cv_show('singel',image)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    images =[]
    for item in contours:
        rect = cv2.boundingRect(item)
        x = rect[0]
        y = rect[1]
        weight = rect[2]
        height = rect[3]
        if (weight > (height * 5)) or (weight < (height * 6)):
            image = origin_image[y:y + height, x:x + weight]
            images.append(image)
    return images
#数字分割
def carLicense_spilte(image):
    gray_image = gray_guss(image)
    ret, image = cv2.threshold(gray_image, 230, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    '''image = cv2.dilate(image, kernel)#膨胀操作
    image = cv2.dilate(image, kernel)#膨胀操作'''
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel,iterations = 1)
    #image = cv2.dilate(image, kernel)#膨胀操作
    #plt_show(image)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    words = []
    word_images = []
    for item in contours:
        word = []
        rect = cv2.boundingRect(item)
        x = rect[0]
        y = rect[1]
        weight = rect[2]
        height = rect[3]
        word.append(x)
        word.append(y)
        word.append(weight)
        word.append(height)
        words.append(word)
    words = sorted(words,key=lambda s:s[0],reverse=False)
    i = 0
    for word in words:
        if  word[3] >=word[2]:#(word[3] > (word[2] * 1.)) and (word[3] < (word[2] * 3.5))
            i = i+1
            splite_image = image[word[1]:word[1] + word[3], word[0]:word[0] + word[2]]
            word_images.append(splite_image)
    return word_images
#模型匹配#####################
#上传文件中的模板图片
def ExtractNum (image):
    lower_screen = []
    up_screen = []
    image = image.astype("uint8")
    led_screen = get_carLicense_img(image)
    for i in range(len(led_screen)):
        if i == 0:
            word_images = carLicense_spilte(led_screen[i])
            for j in range(len(word_images)):
                img = word_images[j]
                img = cv2.resize(img , (128,64))
                #result = svm_predict.predict(img)
                result = Needl.TubeIdentification(img)
                if result == -1:
                    result = 7
                lower_screen.append(result)
        else:
            word_images = carLicense_spilte(led_screen[i])
            for j in range(len(word_images)):
                img = word_images[j]
                img = cv2.resize(img , (128,64))
                #result = svm_predict.predict(img)
                result = Needl.TubeIdentification(img)
                if result == -1:
                    result = 7
                up_screen.append(result)
    return up_screen, lower_screen


if __name__ == "__main__":
    origin_image = cv2.imread('hh.png')
    image = origin_image.copy()
    up , lower = ExtractNum(image)
    print(up)
    print(lower)




