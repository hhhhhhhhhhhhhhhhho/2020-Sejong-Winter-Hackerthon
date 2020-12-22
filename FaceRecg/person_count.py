import face_recognition
import cv2
import numpy as np
import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from DB.Client import client
from gaze_tracking import GazeTracking

class Face:
    def __init__(self, img, id, exam):
        super().__init__()
        self.gaze = GazeTracking()
        self.video_capture = cv2.VideoCapture(0)


        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.count = 0
        self.zerocount =0
        self.img = img
        self.id = id
        self.exam = exam


    def showvideo(self):
        sscount=0
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
                client.cheating(self.id, self.exam, '2',self.frame)
                self.zerocount=0
                cv2.putText(self.frame, "count : "+str(self.count) ,(0,20),font,1.0,(0,0,255),1)
            elif self.count==0:

                #사람이 없을때
                self.zerocount +=1
                if self.zerocount > 100:
                    client.cheating(self.id, self.exam, '2', self.frame)
                    # 자리를 비웠다고 완전히 판단될 때
                    cv2.putText(self.frame, "Away", (120, 20), font, 1.0, (0, 0, 0), 1)
                else:
                    cv2.putText(self.frame, "count : "+str(self.count) ,(0,20),font,1.0,(0,0,0),1)
            else:
                #정상
                self.zerocount=0
                cv2.putText(self.frame, "count : " + str(self.count), (0, 20), font, 1.0, (0, 0, 0), 1)

            # Display the resulting image
            cv2.imshow('Video', self.frame)
            #sscount+=1
            #if sscount==100:
            #    return

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()

    def facecheck(self):
        unknowncnt = 0
        student_img = self.img
        student_face_encoding = face_recognition.face_encodings(student_img)[0]
        known_face_encodings = [student_face_encoding]
        count=0
        known_face_names=[str(count)+"%"]
        while True:
            now = datetime.datetime.now()
            # Grab a single frame of video
            ret, self.frame = self.video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if self.process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        count+=13
                        known_face_names = [str(count) + "%"]
                        name = known_face_names[best_match_index]


                    self.face_names.append(name)

            self.process_this_frame = not self.process_this_frame

            # Display the results
            boxcheck=0

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                if(name=="Unknown"):
                    cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(self.frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    boxcheck == 0
                    unknowncnt+=1
                else:
                    cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(self.frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                boxcheck=1
            if(boxcheck==0):
                count=0
            if(unknowncnt==25):

                client.cheating(self.id,self.exam,'3',self.frame)

            # Display the resulting image
            cv2.imshow('Video', self.frame)
            if(count>=100):
                return
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()

    def hi(self):
        print(self.count)
def start(img):
    vd = Face(img)
    vd.facecheck()
    #vd.showvideo()
    #vd.facecheck()
    #vd.showvideo()

if __name__=='__main__':
    vd = Face()
    vd.facecheck()
    vd.showvideo()




