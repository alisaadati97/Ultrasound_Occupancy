import cv2

baseline_image=None
video=cv2.VideoCapture(0)

while True:
    #Memory usage
    import os, psutil; print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    check, frame = video.read()
    status=0
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
    gray_BGR = cv2.cvtColor(gray_frame ,cv2.COLOR_GRAY2BGR)
    if baseline_image is None:
        baseline_image=gray_frame
        continue

    delta = cv2.absdiff(baseline_image,gray_frame)
    threshold=cv2.threshold(delta, 2, 10, cv2.THRESH_BINARY)[1]
    (_,contours,_) = cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key = cv2.contourArea)
    if cv2.contourArea(contour) < 10000:
            continue
    
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
    cv2.rectangle(gray_BGR, (x, y), (x+w, y+h), (0,255,0), 1)


    cv2.imshow("gray_frame Frame",gray_frame)
    cv2.imshow("Delta Frame",delta)
    cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",gray_BGR)

    key=cv2.waitKey(1)
    baseline_image=gray_frame

    if key==ord('q'):
        break

    if key==ord('s'):
        cv2.imwrite("gray_BGR.png" , gray_BGR)
        cv2.imwrite("threshold.png" , threshold)
        break

#Clean up, Free memory
video.release()
cv2.destroyAllWindows