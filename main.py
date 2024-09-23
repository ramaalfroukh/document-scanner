######DOC SCANNER
import cv2
import numpy as np
from numpy.ma.testutils import approx
from numpy.matrixlib.defmatrix import matrix

#################### create initail parametrs
cap=cv2.VideoCapture(0)
cap.set(10,160) # the brightneees of the cam
heightImg=640
widthImg=480
#################################

def processinng(img):
  imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #to change the color of imge to gray
  imgBlur=cv2.GaussianBlur(imggray,(5,5),1) # to change grayimg to blur to know the corners of peaper
  imgCanny=cv2.Canny(imgBlur,200,200)  #to change the imgblur to black

  Kernal=np.ones((5,5)) #عشان يحدد الزوايا ويخليهم واضحين ويعرض الخط
  imgDial=cv2.dilate(imgCanny,Kernal,iterations=2)
  imgThres=cv2.erode(imgDial,Kernal,iterations=1)

  return imgThres

def getContours(img):#لايجاد الحواف للورقة
    biggest=np.array([])
    maxArea=0
    contours,hirachy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours: #كل الزوايا اللي تعرف عليها
      area = cv2.contourArea(cnt)# لحساب المساحة الخاصة بالورقة واالحواف

      if area>1000: #حسب حجم الكاميرا ووضوحها بتضل تجلرب عبين م يتعرف الكود على الكتابة اللي عالورقة
          peri=cv2.arcLength(cnt,True) #عشان يحسب كم زاوية في وترو يعني الشكل مغلق
          approx=cv2.approxPolyDP(cnt,0.02*peri,True)
          if area>maxArea and len(approx)==4: #اذا كان عدد الزوايا 4
            biggest=approx
            maxArea=area
            cv2.drawContours(imgContour, [biggest], -1, (0, 0, 255),
                             3)  # لرسم الحواف -1 حتى نتعرف على جميع الحواف وال 255 هواللون الاحمر


    return biggest


def reorder(points):
  points=points.reshape((4,2))
  newPoints=np.zeros((4,1,2),np.int32)
  add=points.sum(1)
  newPoints[0]=points[np.argmin(add)]
  newPoints[2]=points[np.argmax(add)]

  diff=np.diff(Points,axis=1)

  newPoints[1]=points[np.argmin(diff)]
  newPoints[3]=points[np.argmax(diff)]

  return newPoints




def wrap(img,biggest,imgsize): #بقص الورقة من الفيديو
  widthImg=imgsize[0]
  heightImg=imgsize[1]
  biggest=reorder(biggest)
  pts1=np.float32(biggest) #النقطة الاولى
  pts2=np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])

  matrix = cv2.getPerspectiveTransform(pts1,pts2)
  imgOutput=cv2.warpPerspective(img,matrix,(widthImg,heightImg))

  imgCropped=imgOutput[20:imgoutput.shape[0]-20,20:imgoutput.shape[1]-20]
  imgCropped=cv2.resize(imgCropped,(widthImg,heightImg))


  return imgCropped


while True :
    _,img= cap.read()
    imgContour=img.copy() #باخد من الصوره الاصليه كوبي عشان اعدل عليها براحتي
    imgSize=img.shape
    processrdimg = processinng(img)
    biggest=getContours(processrdimg)
    getContours(processrdimg)

    if biggest.size !=0:
        imgWarped=wrap(img,biggest,imgSize)
        key=cv2.waitKey(1)
        if key ==ord('s'):# to save when enter s
            cv2.imwrite('myDoc.jpg',imgWarped)
        cv2.imshow('Doc',imgWarped)
    else :
        pass



    cv2.imshow('img',imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break



