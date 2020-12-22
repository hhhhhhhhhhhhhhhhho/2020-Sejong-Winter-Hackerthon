import face_recognition
import cv2
import numpy as np
import datetime
from gaze_tracking import GazeTracking

class Face:
    def __init__(self):
        super().__init__()
        self.gaze = GazeTracking()
        self.video_capture = cv2.VideoCapture(0)


        self.face_locations = []
        self.face_encodings = []

        self.process_this_frame = True
        self.count = 0
        self.zerocount =0
    def showvideo(self):

        while True:
            now = datetime.datetime.now()
            # 1프레임씩 가져오기
            ret, self.frame = self.video_capture.read()
            self.gaze.refresh(self.frame)
            self.frame = self.gaze.annotated_frame()
            text = ""
            if self.gaze.is_blinking():
                text = "Blinking"
            elif self.gaze.is_right():
                text = "Looking right"
            elif self.gaze.is_left():
                text = "Looking left"
            elif self.gaze.is_center():
                text = "Looking center"

            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)


            rgb_small_frame = small_frame[:, :, ::-1]

            left_pupil = self.gaze.pupil_left_coords()
            right_pupil = self.gaze.pupil_right_coords()
            cv2.putText(self.frame, "Left eye:  " + str(left_pupil), (0, 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(self.frame, "Right eye: " + str(right_pupil), (0, 85), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(self.frame, text, (0, 120), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            f = open("eyes.txt",'a')
            data =str(left_pupil)+str(right_pupil)+"\n"
            f.write(data)
            f.close()
            if self.process_this_frame:

                self.face_locations = face_recognition.face_locations(rgb_small_frame)


            self.process_this_frame = not self.process_this_frame

            self.count = 0

            for (top, right, bottom, left) in self.face_locations:

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                self.count+=1
                # Draw a box around the face
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX


            if self.count>=2:
                #사람이 두명 이상일 때
                self.zerocount=0
                cv2.putText(self.frame, "count : "+str(self.count) ,(0,20),font,1.0,(0,0,255),1)
            elif self.count==0:
                #사람이 없을때
                self.zerocount +=1
                if self.zerocount > 100:
                    # 자리를 비웠다고 완전히 판단될 때
                    cv2.putText(self.frame, "Away", (120, 20), font, 1.0, (0, 0, 0), 1)
                else:
                    cv2.putText(self.frame, "count : "+str(self.count) ,(0,20),font,1.0,(0,0,0),1)
            else:
                #정상
                self.zerocount=0
                cv2.putText(self.frame, "count : " + str(self.count), (0, 20), font, 1.0, (0, 0, 0), 1)




            # Display the resulting image
            #cv2.imshow('Video', self.frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video_capture.release()
        cv2.destroyAllWindows()
if __name__=='__main__':
    vd = Face()
    vd.showvideo()
