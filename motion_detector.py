import  cv2

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)                          #capture video

first_frame = None                                                  #assigning None to first_frame

while True:
    check, frame = video.read()                                     #reading video to frame in loop

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            #converting to gray for detection easiness

    gray_frame = cv2.GaussianBlur(gray_frame, (21,21),0)            #making the image blur for reducing noise

    if first_frame is None:
        first_frame=gray_frame                                       #storing first frame 
        continue


    delta_frame = cv2.absdiff(first_frame, gray_frame)               #comparing first frame with remaining frames
    
    cv2.imshow("gray frame", gray_frame)                             #showing gray frames

    cv2.imshow("delta frame", delta_frame)                            #showing the difference of frames



    key = cv2.waitKey(1) 

    print(gray_frame)                                                 #print numpy array

    if key==ord('q'):                                                 #if q is pressed break the loop
        break




video.release()  

cv2.destroyAllWindows
