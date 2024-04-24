import cv2
import imutils
import numpy as np
import serial
import time 

cam = cv2.VideoCapture(0)
# arduino =serial.Serial('COM7',9600,timeout=1)
count = 0
nil_kernel =3

def loadconfig():
    global Humin,Sumin,Vumin,Humax,Sumax,Vumax
    global Hmmin,Smmin,Vmmin,Hmmax,Smmax,Vmmax
    global Hpmin,Spmin,Vpmin,Hpmax,Spmax,Vpmax
    f = open("dataThreshold.txt","r")
    for line in f.readlines():
        arr_read =line.split(',')
        Humin = int(arr_read[0])
        Sumin = int(arr_read[1])
        Vumin = int(arr_read[2])
        Humax = int(arr_read[3])
        Sumax = int(arr_read[4])
        Vumax = int(arr_read[5])
        Hmmin = int(arr_read[6])
        Smmin = int(arr_read[7])
        Vmmin = int(arr_read[8])
        Hmmax = int(arr_read[9])
        Smmax = int(arr_read[10])
        Vmmax = int(arr_read[11])
        Hpmin = int(arr_read[12])
        Spmin = int(arr_read[13])
        Vpmin = int(arr_read[14])
        Hpmax = int(arr_read[15])
        Spmax = int(arr_read[16])
        Vpmax = int(arr_read[17])
        f.close
    print('loaded')
    
def saveconfig():
    global Humin,Sumin,Vumin,Humax,Sumax,Vumax
    global Hmmin,Smmin,Vmmin,Hmmax,Smmax,Vmmax
    global Hpmin,Spmin,Vpmin,Hpmax,Spmax,Vpmax
    f = open("dataThreshold.txt","w")
    data0= '%d,%d,%d,%d,%d,%d'%(Humin,Sumin,Vumin,Humax,Sumax,Vumax)
    data1= '%d,%d,%d,%d,%d,%d'%(Hmmin,Smmin,Vmmin,Hmmax,Smmax,Vmmax)
    data2= '%d,%d,%d,%d,%d,%d'%(Hpmin,Spmin,Vpmin,Hpmax,Spmax,Vpmax)
    data =data0 +',' + data1 +',' +data2
    f.write(data)
    f.close
    print('saved')
    

def setControl(count):
    global Humin,Sumin,Vumin,Humax,Sumax,Vumax
    global Hmmin,Smmin,Vmmin,Hmmax,Smmax,Vmmax
    global Hpmin,Spmin,Vpmin,Hpmax,Spmax,Vpmax
    
    
    if count==0:
        a=Humin
        b=Sumin
        c=Vumin
        d=Humax
        e=Sumax
        f=Vumax
        
    elif count==1:
        a=Hmmin
        b=Smmin
        c=Vmmin
        d=Hmmax
        e=Smmax
        f=Vmmax
        
    elif count==2:
        a=Hpmin
        b=Spmin
        c=Vpmin
        d=Hpmax
        e=Spmax
        f=Vpmax
    
    def nothing(x):
        pass
    
    
    
    cv2.namedWindow('setting masking')
    cv2.resizeWindow('setting masking',600,300)
    cv2.createTrackbar('Hmin','setting masking',a,180,nothing)
    cv2.createTrackbar('Smin','setting masking',b,255,nothing)
    cv2.createTrackbar('Vmin','setting masking',c,255,nothing)
    cv2.createTrackbar('Hmax','setting masking',d,180,nothing)
    cv2.createTrackbar('Smax','setting masking',e,255,nothing)
    cv2.createTrackbar('Vmax','setting masking',f,255,nothing)
    

def setTrackbar(a,b,c,d,e,f):
    cv2.setTrackbarPos('Hmin','setting masking',a)
    cv2.setTrackbarPos('Smin','setting masking',b)
    cv2.setTrackbarPos('Vmin','setting masking',c)
    cv2.setTrackbarPos('Hmax','setting masking',d)
    cv2.setTrackbarPos('Smax','setting masking',e)
    cv2.setTrackbarPos('Vmax','setting masking',f)
    
def programhelp():
    print('')
    print('=========MENU 2========')
    print('1. destroAllWindows--------[q]')
    print('2. Save Data---------------[s]')
    print('3. Ganti Mode--------------[t]')
    print('==================')
    print('')
    
    
def Tanding():
    global Humin,Sumin,Vumin,Humax,Sumax,Vumax
    global Hmmin,Smmin,Vmmin,Hmmax,Smmax,Vmmax
    global Hpmin,Spmin,Vpmin,Hpmax,Spmax,Vpmax
    loadconfig()
    
    
    while(1):
        u_lower_val = np.array([Humin,Sumin,Vumin])
        u_upper_val = np.array([Humax,Sumax,Vumax])
        
        m_lower_val = np.array([Hmmin,Smmin,Vmmin])
        m_upper_val = np.array([Hmmax,Smmax,Vmmax])
        
        p_lower_val = np.array([Hpmin,Spmin,Vpmin])
        p_upper_val = np.array([Hpmax,Spmax,Vpmax])
        
        ret,frame = cam.read()
        frame = cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
        
        if not ret:
            break
        
        mask_ungu = cv2.inRange(hsv.copy(),u_lower_val,u_upper_val)
        mask_merah = cv2.inRange(hsv.copy(),m_lower_val,m_upper_val)
        mask_putih = cv2.inRange(hsv.copy(),p_lower_val,p_upper_val)
        
        
        
        kernel= np.ones((nil_kernel,nil_kernel),np.uint8)
        mask_ungu=cv2.morphologyEx(mask_ungu,cv2.MORPH_OPEN,kernel,iterations=1)
        mask_merah=cv2.morphologyEx(mask_merah,cv2.MORPH_OPEN,kernel,iterations=1)
        mask_putih=cv2.morphologyEx(mask_putih,cv2.MORPH_OPEN,kernel,iterations=1)
        
        contour1,hierarchy = cv2.findContours(mask_ungu,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        contour2,hierarchy = cv2.findContours(mask_merah,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        contour3,hierarchy = cv2.findContours(mask_putih,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        if len(contour1) > 0:
            for cnt in contour1:
                area= cv2.contourArea(cnt)
                if area>50:
                    hull = cv2.convexHull(cnt)
                    cv2.drawContours(frame,[hull],-1,(0,0,255),4)
                    area_str = str(area)
                    # arduino.write(area_str.encode()+ b'\n')
                    print("Sent area to Arduino:", area_str)
                    time.sleep(0.005)
                    
        if len(contour2) > 0:
            for cnt in contour2:
                area= cv2.contourArea(cnt)
                if area>50:
                    hull = cv2.convexHull(cnt)
                    cv2.drawContours(frame,[hull],-1,(0,0,255),4)
                    
        if len(contour3) > 0:
            for cnt in contour3:
                area= cv2.contourArea(cnt)
                if area>50:
                    hull = cv2.convexHull(cnt)
                    cv2.drawContours(frame,[hull],-1,(0,0,255),4)
                    
        k =cv2.waitKey(1) & 0xff
        if k==ord('q'):
            cv2.destroyAllWindows()
            break
        
        cv2.imshow('res',frame)
        # cv2.imshow('mask',mask)
        
        
        
    

def SetData():
    global Humin,Sumin,Vumin,Humax,Sumax,Vumax
    global Hmmin,Smmin,Vmmin,Hmmax,Smmax,Vmmax
    global Hpmin,Spmin,Vpmin,Hpmax,Spmax,Vpmax
    global Lower_val,Upper_val
    global frame,count
    loadconfig()
    setControl(0)
    programhelp()

    
    while (1):
       
        Hmin= cv2.getTrackbarPos('Hmin','setting masking')
        Smin= cv2.getTrackbarPos('Smin','setting masking')
        Vmin= cv2.getTrackbarPos('Vmin','setting masking')
        Hmax= cv2.getTrackbarPos('Hmax','setting masking')
        Smax= cv2.getTrackbarPos('Smax','setting masking')
        Vmax= cv2.getTrackbarPos('Vmax','setting masking')
        
        Lower_val = np.array([Hmin,Smin,Vmin])
        Upper_val = np.array([Hmax,Smax,Vmax])
        
        ret,frame = cam.read()
        frame = cv2.flip(frame,1)
        hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask= cv2.inRange(hsv,Lower_val,Upper_val)
        
        kernel= np.ones((10,10),np.uint8)
        mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel,iterations=1)
        
        contour,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        if len(contour) > 0:
            for cnt in contour:
                area= cv2.contourArea(cnt)
                if area>100:
                    hull = cv2.convexHull(cnt)
                    cv2.drawContours(frame,[hull],-1,(0,0,255),4)
        
        
        
        if not ret:
            break
        
        if count==0:
            cv2.putText(frame,'UNGU',(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,(50,168,50),2,cv2.FILLED)
        elif count==1:
            cv2.putText(frame,'BIRU',(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,(50,168,50),2,cv2.FILLED)
        elif count==2:    
            cv2.putText(frame,'PUTIH',(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,(50,168,50),2,cv2.FILLED)
            
        
        
        k =cv2.waitKey(1) & 0xff
        if k==ord('q'):
            cv2.destroyAllWindows()
            break
        if k==ord('t'):
            count=count +1
            if count>2:
                count=0
            
            if count==0:
                a=Humin
                b=Sumin
                c=Vumin
                d=Humax
                e=Sumax
                f=Vumax
        
            elif count==1:
                a=Hmmin
                b=Smmin
                c=Vmmin
                d=Hmmax
                e=Smmax
                f=Vmmax
        
            elif count==2:
                a=Hpmin
                b=Spmin
                c=Vpmin
                d=Hpmax
                e=Spmax
                f=Vpmax
            setTrackbar(a,b,c,d,e,f)
        
        
        if k==ord('s'):
            if count==0:
                Humin=Hmin
                Sumin=Smin
                Vumin=Vmin
                Humax=Hmax
                Sumax=Smax
                Vumax=Vmax
                saveconfig()
            elif count==1:
                Hmmin=Hmin
                Smmin=Smin
                Vmmin=Vmin
                Hmmax=Hmax
                Smmax=Smax
                Vmmax=Vmax
                saveconfig()
            elif count==2:
                Hpmin=Hmin
                Spmin=Smin
                Vpmin=Vmin
                Hpmax=Hmax
                Spmax=Smax
                Vpmax=Vmax
                saveconfig()
                
        cv2.imshow('res',frame)
        cv2.imshow('mask',mask)
        
        
        
def proghelp():
    print('')
    print('===========MENU===============')
    print('start----------------------[m]')
    print('Setting Threshold----------[s]')
    print('Destroy all windows--------[q]')
    print('==============================')
    print('')

'''===============PROGRAM UTAMA============='''
while (1):
    proghelp()
    img= cv2.imread('cadiak pandai.jpg')
    img =imutils.resize(img,400)
    cv2.imshow('logo tim',img)
    k =cv2.waitKey(0) & 0xff
    if k==ord('s'):
        SetData()
    elif k==ord('q'):
        break
    elif k==ord('m'):
        Tanding()
cam.release()
cv2.destroyAllWindows()
