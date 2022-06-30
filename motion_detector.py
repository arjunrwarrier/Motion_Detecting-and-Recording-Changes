from datetime import datetime
import  cv2,time,pandas

first_frame = None                                                  #assigning None to first_frame

status_list = [None,None]                                           #added None to avoid list index error in times.append()

times = []                                                          #for adding the times to a list

df = pandas.DataFrame(columns=["Start","End"])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)                          #capture video
#time.sleep(1)
                                                 

while True:
    check, frame = video.read()                                     #reading video to frame in loop

    status = 0                                                      # motion detection status status

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            #converting to gray for detection easiness

    gray_frame = cv2.GaussianBlur(gray_frame, (21,21),0)            #making the image blur for reducing noise

    if first_frame is None:
        first_frame=gray_frame                                       #storing first frame 
        continue


    delta_frame = cv2.absdiff(first_frame, gray_frame)               #comparing first frame with remaining frames
    thresh_frame = cv2.threshold(delta_frame, 80,255,cv2.THRESH_BINARY)[1]#adding a threshold frame change values given accordingly
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)           #smoothening the threshold frame

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #finding cotours by passing copy of thresh frame
    #external contours are taken, and approximation method by opencv for applying it.

    
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:                              #checking if area of contour is less than 1000, true=loop again, false=execute next lines
            continue
        status =1                                                        #changing status
        (x,y,w,h) = cv2.boundingRect(contour)                            #drawing rectangle on the moving object
        cv2.rectangle(frame, (x,y),(x+w, y+h),(0,255,0),3)               #assinging positions and colors

    status_list.append(status)

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())





    cv2.imshow("gray frame", gray_frame)                             #showing gray frames

    cv2.imshow("delta frame", delta_frame)                            #showing the difference of frames

    cv2.imshow("thresh frame",thresh_frame)

    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1) 

    

    if key==ord('q'):                                                 #if q is pressed break the loop
        if status ==1:
            times.append(datetime.now())
        break

    
print(status_list)                                                   #for reference

print(times)                                                         #for reference

for i in range(0,len(times),2):                                     #from 0 to len(times) with step 2 for skipping the motion end time
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True) #adding values to dataframe

df.to_csv("Times.csv")                                                #saving it as a csv file




video.release()  

cv2.destroyAllWindows()
