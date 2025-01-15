import cv2

img1 = cv2.imread('1.jpg')
img2 = cv2.imread('1.jpg')
img3 = cv2.imread('1.jpg')

height , width , layers =  img1.shape

#video = cv2.VideoWriter('video.avi',-1,1,(width,height))
video = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'),1,(width,height))

video.write(img1)
video.write(img2)
video.write(img3)

cv2.destroyAllWindows()
video.release()
