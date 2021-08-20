from cv2 import cv2
def Iswhite(image, row_start, row_end, col_start, col_end):
    white_num = 0
    j=row_start
    i=col_start
 
    while(j <= row_end):
        while(i <= col_end):
            if(image[j][i] == 255):                
                white_num+=1
            i+=1
        j+=1
        i=col_start
    #print('white num is',white_num)
    if(white_num >= 5):
        return True
    else:
        return False
def TubeIdentification( image):
    tube = 0
    tubo_roi = [
         [image.shape[0] * 0/3, image.shape[0] * 1/3, image.shape[1] * 1/2, 
                                                      image.shape[1] * 1/2],
         [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 2/3, 
                                                      image.shape[1] - 1  ],
         [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 2/3, 
                                                      image.shape[1] - 1  ],
         [image.shape[0] * 2/3, image.shape[0] -1   , image.shape[1] * 1/2, 
                                                      image.shape[1] * 1/2],
         [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 0/3, 
                                                      image.shape[1] * 1/3],
         [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 0/3, 
                                                      image.shape[1] * 1/3],
         [image.shape[0] * 1/3, image.shape[0] * 2/3, image.shape[1] * 1/2, 
                                                      image.shape[1] * 1/2]] 
    i = 0
    while(i < 7):
        if(Iswhite(image, int(tubo_roi[i][0]), int(tubo_roi[i][1]), 
            int(tubo_roi[i][2]),int(tubo_roi[i][3]))):
            tube = tube + pow(2,i)
            
        cv2.line(image, ( int(tubo_roi[i][3]),int(tubo_roi[i][1])), 
                (int(tubo_roi[i][2]), int(tubo_roi[i][0])),                
                (255,0,0), 1)                       
        i += 1
 
    if(tube==63):
        onenumber = 0
    elif(tube==6):
        onenumber = 1
    elif(tube==91):
        onenumber = 2
    elif(tube==79):
        onenumber = 3
    elif(tube==102 or tube==110):
    #110是因为有干扰情况
        onenumber = 4
    elif(tube==109):
        onenumber = 5
    elif(tube==125):
        onenumber = 6
    elif(tube==7):
        onenumber = 7
    elif(tube==127):
        onenumber = 8
    elif(tube==103):
        onenumber = 9
    else:
        onenumber = -1 
    return onenumber