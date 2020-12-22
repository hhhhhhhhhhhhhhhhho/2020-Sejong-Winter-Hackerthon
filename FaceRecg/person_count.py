import face_recognition
import cv2
import numpy as np
import datetime
from gaze_tracking import GazeTracking

gaze = GazeTracking()

video_capture = cv2.VideoCapture(0)


face_locations = []
face_encodings = []
face_names = ["kim"]
process_this_frame = True
count = 0
zerocount =0

while True:
    now = datetime.datetime.now()
    # 1프레임씩 가져오기
    ret, frame = video_capture.read()
    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    text = ""
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


    rgb_small_frame = small_frame[:, :, ::-1]

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left eye:  " + str(left_pupil), (0, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right eye: " + str(right_pupil), (0, 85), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, text, (0, 120), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)


    process_this_frame = not process_this_frame

    count = 0

    for (top, right, bottom, left) in face_locations:

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        count+=1
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)




    font = cv2.FONT_HERSHEY_DUPLEX


    if count>=2:
        #사람이 두명 이상일 때
        zerocount=0
        cv2.putText(frame, "count : "+str(count) ,(0,20),font,1.0,(0,0,255),1)
    elif count==0:
        #사람이 없을때
        zerocount +=1
        if zerocount > 100:
            # 자리를 비웠다고 완전히 판단될 때
            cv2.putText(frame, "Away", (120, 20), font, 1.0, (0, 0, 0), 1)
        else:
            cv2.putText(frame, "count : "+str(count) ,(0,20),font,1.0,(0,0,0),1)
    else:
        #정상
        zerocount=0
        cv2.putText(frame, "count : " + str(count), (0, 20), font, 1.0, (0, 0, 0), 1)



    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
