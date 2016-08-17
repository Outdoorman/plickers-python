# -*-coding:utf-8-*-
import cv2
import numpy as np
from my_math import  Math
from time import sleep
import pickle
import sys

global CARD_NUM

CARD_NUM=1
def card_check(result):
    global CARD_NUM
    count = 1
    wigth,higth=result.shape
    result=cv2.resize(result,(10*higth,10*wigth))
    card_array = np.zeros([5, 5])  # array sort [y,x]
    wigth,higth=result.shape
    #print 'check',wigth,higth
    for y in range(1, 6):
        for x in range(1, 6):
            # print 'con',count,y,x
            # print (higth)* (y/5.0)
            if y == 1 and x == 1:
                crop = result[0:int(wigth * (y / 5.0)), 0:int(wigth * (x / 5.0))]
            elif y == 1:
                crop = result[0:int(wigth * (y / 5.0)), int(wigth * ((x - 1) / 5.0)):int(wigth * (x / 5.0))]
                #print int(wigth*(y/5.0)),int(wigth*((x-1)/5.0)),int(wigth*(x/5.0))
                # cv2.imshow(str(y)+':'+str(x), crop)
                # cv2.waitKey(0)
            elif x == 1:
                crop = result[int(wigth * ((y - 1) / 5.0)):int(wigth * (y / 5.0)), 0:int(wigth * (x / 5.0))]
            else:
                crop = result[int(wigth * ((y - 1) / 5.0)):int(wigth * (y / 5.0)),
                       int(wigth * ((x - 1) / 5.0)):int(wigth * (x / 5.0))]

            if np.average(crop) > 120:
                #1 is white  0 is balck
                card_array[y - 1, x - 1] = 0
            else:
                card_array[y - 1, x - 1] = 1
            count += 1

    num = 0
    check = 0
    print 'the global num',CARD_NUM,'the card',card_array
    for i in card_data:
        # print i
        if np.array_equal(i, card_array):
            check = 1
            break
        num += 1
    if check:
        print 'the global num',CARD_NUM,num, 'bingo',card_list[num]
        return card_list[num]
    CARD_NUM+=1
    return 0

#####读取卡片的矩阵信息#######
np.set_printoptions(threshold='nan')

fn= '/home/project/camera/card.data'
f=open(fn,'rb').read()
card_data=pickle.loads(f)
fn= '/home/project/camera/card.list'
f=open(fn,'rb').read()
card_list=pickle.loads(f)
#print len(card_list)
#print card_list
#print card_data


#############main####################
img = cv2.imread('./senshoot/DSC_0570.JPG')
w,h,s=img.shape
print img.shape
img=cv2.resize(img,(int(h/2.0),int(w/2.0)))
###模糊###
img = cv2.GaussianBlur(img,(3,3),0)

###描边###
canny = cv2.Canny(img, 40, 170)

###转换成灰度图###
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
###转换成黑白图片###
ret, thresh = cv2.threshold(gray, 99, 255, 1)

###寻找边框###
nimg, contours, h = cv2.findContours(canny,2,1)

for cnt in contours:
    if len(cnt) >50:
        #print 'now',cnt
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if len(approx) > 4:

            #maybe_card=thresh[cnt[:,0,:].min():cnt[:,0,:].max(),cnt[:,:,0].min():cnt[:,:,0].max()]
            #maybe_canny=canny[cnt[:,0,:].min():cnt[:,0,:].max(),cnt[:,:,0].min():cnt[:,:,0].max()]
            if cnt[:,0,:].max() - cnt[:,0,:].min() >cnt[:,:,0].max()- cnt[:,:,0].min():
                diff=cnt[:,:,0].max()-cnt[:,:,0].min()
                card=thresh[cnt[:,0,:].min():cnt[:,0,:].min()+diff, cnt[:,:,0].min():cnt[:,:,0].max()  ]
                if  len(card)>10 and np.average(card)<230 and np.average(card)>100:
                    card_check(card)
                card=thresh[abs(cnt[:,0,:].max()-diff):cnt[:,0,:].max(), cnt[:,:,0].min():cnt[:,:,0].max()  ]
                if  len(card)>10 and np.average(card)<230 and np.average(card)>100:
                    card_check(card)
            else:

                diff=cnt[:,0,:].max()-cnt[:,0,:].min()
                card=thresh[cnt[:,0,:].min():cnt[:,0,:].max(), cnt[:,:,0].min():cnt[:,:,0].min()+diff  ]
                if  len(card)>10 and np.average(card)<230 and np.average(card)>100:
                    card_check(card)
                card=thresh[cnt[:,0,:].min():cnt[:,0,:].max(), cnt[:,:,0].max()-diff:cnt[:,:,0].max()  ]
                if  len(card)>10 and np.average(card)<230 and np.average(card)>100:
                    card_check(card)



