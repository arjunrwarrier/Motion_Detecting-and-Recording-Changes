import  cv2
import time

first_frame = None                                                  #assigning None to first_frame

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)                          #capture video
time.sleep(1)
                                                 

while True:
    check, frame = video.read()                                     #reading video to frame in loop

    status = 0                                                      # motion detection status status

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            #converting to gray for detection easiness

    gray_frame = cv2.GaussianBlur(gray_frame, (21,21),0)            #making the image blur for reducing noise

    if first_frame is None:
        first_frame=gray_frame                                       #storing first frame 
        continue


    delta_frame = cv2.absdiff(first_frame, gray_frame)               #comparing first frame with remaining frames
    thresh_frame = cv2.threshold(delta_frame, 100,255,cv2.THRESH_BINARY)[1]#adding a threshold frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)           #smoothening the threshold frame

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #finding cotours by passing copy of thresh frame
    #external contours are taken, and approximation method by opencv for applying it.

    
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:                              #checking if area of contour is less than 1000, true=loop again, false=execute next lines
            continue
        status =1                                                        #changing status
        (x,y,w,h) = cv2.boundingRect(contour)                            #drawing rectangle on the moving object
        cv2.rectangle(frame, (x,y),(x+w, y+h),(0,255,0),3)               #assinging positions and colors




    cv2.imshow("gray frame", gray_frame)                             #showing gray frames

    cv2.imshow("delta frame", delta_frame)                            #showing the difference of frames

    cv2.imshow("thresh frame",thresh_frame)

    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1) 

    

    if key==ord('q'):                                                 #if q is pressed break the loop
        break

    print(status)


video.release()  

cv2.destroyAllWindows()
