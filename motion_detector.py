import  cv2

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("capture", gray_frame)

    key = cv2.waitKey(1)

    print(gray_frame)

    if key==ord('q'):
        break




video.release()

cv2.destroyAllWindows