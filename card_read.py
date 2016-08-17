from scipy.odr.odrpack import odr_stop
import cv2
import numpy as np
from my_math import  Math
from time import sleep
import os

import scipy



def card_read(img):
    dst = cv2.blur(img,(3,3))
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    np.set_printoptions(threshold='nan')


    #gray = cv2.imread('img.jpg', 0)
    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    #ret, thresh = cv2.threshold(gray, 127, 255, 1)
    nimg, contours, h = cv2.findContours(thresh,2,1)
    #nimg, contours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if len(cnt) >500:
            #print 'now',cnt
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            # print len(approx)
            if len(approx) > 11:
                print 'square'
                print 'cnt len',len(cnt)
                print 'shape',cnt.shape
                print 'x max ',cnt[:,:,0].max(),'x min',cnt[:,:,0].min()
                print cnt[:,:,0].mean()
                x_leter,x_biger,y_leter,y_biger=[],[],[],[]

                for i in  cnt[:,:,0].tolist():
                    if i[0] >  cnt[:,:,0].mean():
                        x_biger.append(i[0])
                    else:
                        x_leter.append(i[0])

                for i in  cnt[:,:,1].tolist():
                    if i[0] >  cnt[:,:,1].mean():
                        y_biger.append(i[0])
                    else:
                        y_leter.append(i[0])


                x_biger_mode=Math.mode(x_biger)
                x_leter_mode=Math.mode(x_leter)
                y_biger_mode=Math.mode(y_biger)
                y_leter_mode=Math.mode(y_leter)
                print x_biger_mode,x_leter_mode
                #a,b,c,d= cnt[0][0],cnt[int(len(cnt)*0.33)][0],cnt[len(cnt)*0.66][0],cnt[-1][0] #

                #card=gray[y_leter_mode[0]:y_biger_mode[0],x_leter_mode[0]:x_biger_mode[0]]
                card=gray[cnt[:,0,:].min():cnt[:,0,:].max(),cnt[:,:,0].min():cnt[:,:,0].max()]
                retval, result = cv2.threshold(card, 90, 255, cv2.THRESH_BINARY)
                wigth,higth=card.shape
                #cv2.imshow('card',card)
                #cv2.waitKey(0)
                print wigth,higth,type(wigth),type(higth)
                count=1
                card_array=np.zeros([5,5]) #array sort [y,x]
                for y in range(1,6):
                    for x in range(1,6):
                        back_while=0
                        print 'now local',int(higth*y/5.0),int(wigth*x/5.0)
                        if y ==1 and x==1:
                            crop=result[0:int(higth*(y/5.0)),0:int(wigth*(x/5.0))]
                        elif y ==1:
                            crop=result[0:int(higth*(y/5.0)),int(wigth*((x-1)/5.0)):int(wigth*(x/5.0))]
                            #print int(wigth*(y/5.0)),int(wigth*((x-1)/5.0)),int(wigth*(x/5.0))
                            #cv2.imshow(str(y)+':'+str(x), crop)
                            #cv2.waitKey(0)
                        elif x==1:
                            crop=result[int(higth*((y-1)/5.0)):int(higth*(y/5.0)),0:int(wigth*(x/5.0))]
                        else:
                            crop=result[int(higth*((y-1)/5.0)):int(higth*(y/5.0)),int(wigth*((x-1)/5.0)):int(wigth*(x/5.0))]

                        if np.average(crop) > 200:
                            back_while=1
                            card_array[y-1,x-1]=1
                        else:
                            card_array[y-1,x-1]=0
                        print 'con',count,y,x,back_while,np.average(crop)
                        count+=1
                return card_array

import pickle
if __name__ == '__main__':
    file_list =os.listdir('/home/project/camera/card_file/')
    card_data=[]
    card_list=[]
    for file in file_list:
        img = cv2.imread('./card_file/'+file)
        #img = cv2.imread('./card_file/'+'033-C.jpg')
        file_name=file.split('.')[0]
        file_num,option=file_name.split('-')

        card_array=card_read(img)

        print 'file',file_num,option
        print card_array
        if option=='A':
            A=card_array
            B=np.rot90(card_array,1)
            C=np.rot90(card_array,2)
            D=np.rot90(card_array,3)
        elif option=='B':
            A=np.rot90(card_array,3)
            B=card_array
            C=np.rot90(card_array,1)
            D=np.rot90(card_array,2)
        elif option=='C':
            C=card_array
            D=np.rot90(card_array,1)
            A=np.rot90(card_array,2)
            B=np.rot90(card_array,3)
        else:
            D=card_array
            A=np.rot90(card_array,1)
            B=np.rot90(card_array,2)
            C=np.rot90(card_array,3)
        card_data.extend(i for i in [A,B,C,D])
        card_list.extend(file_num+'-'+i for i in ['A','B','C','D'])
        del img,file_name,file_num,option,card_array
    fn= 'card.data'
    with open(fn, 'wb') as f: # open file with write-mode
        picklestring = pickle.dump(card_data, f)

    fl= 'card.list'
    with open(fl, 'wb') as ff: # open file with write-mode
        picklestring = pickle.dump(card_list, ff)