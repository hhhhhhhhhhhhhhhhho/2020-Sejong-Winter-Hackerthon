import cv2
import numpy as np
import dlib
#import matplotlib.pyplot as plt
import pandas as pd
# Load the detector
import csv
import main # AI main
import torch
#import tensorflow as tf

detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("facial-landmarks-recognition/shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)


'''
# read the image
# img = cv2.imread("face.jpg")
'''
def detection_cheat_for_eye():
    cnt = 0
    memory_cord = [(0,0)]
    memory_cord_right = [(0,0)]
    while(True):

        ret, frame = cap.read()
        if not ret:
            raise NotImplementedError

        gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

        # Use detector to find landmarks
        faces = detector(gray)

        for face in faces:
            x1 = face.left() # left point
            y1 = face.top() # top point
            x2 = face.right() # right point
            y2 = face.bottom() # bottom point
            # Create landmark object
            landmarks = predictor(image=gray, box=face)
            left_eye_x = []
            left_eye_y = []
            for n in range(36, 42):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                left_eye_x.append(x)
                left_eye_y.append(y)
                # cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 255), thickness=-1)
                # yellow : left eye

            # left
            left_max_x = max(left_eye_x)
            left_min_x = min(left_eye_x)
            left_max_y = max(left_eye_y)
            left_min_y = min(left_eye_y)
            left_lefttop = (left_min_x, left_min_y)
            left_center = ((left_max_x + left_min_x) // 2, (left_max_y + left_min_y) // 2)
            if not (left_center[0] <= 2 or left_center[1] <= 2) :
                cv2.circle(img=frame, center=left_center, radius=1, color=(0, 255, 255), thickness=-1)

            right_eye_x = []
            right_eye_y = []
            for n in range(42, 48):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                right_eye_x.append(x)
                right_eye_y.append(y)
                # cv2.circle(img=frame, center=(x, y), radius=3, color=(0, 255, 0), thickness=-1)
                # green : right eye

            # right
            right_max_x = max(right_eye_x)
            right_min_x = min(right_eye_x)
            right_max_y = max(right_eye_y)
            right_min_y = min(right_eye_y)
            right_lefttop = (right_min_x, right_min_y)
            right_center = ((right_max_x + right_min_x)// 2, (right_max_y + right_min_y)//2)
            #print(right_center)
            if not (right_center[0] <= 2 or right_center[1] <= 2) :
                cv2.circle(img=frame, center=right_center, radius=1, color=(0, 255, 0), thickness=-1)

            left_eye_im = frame[min(left_eye_y):max(left_eye_y), min(left_eye_x):max(left_eye_x), :].copy()
            right_eye_im = frame[min(right_eye_y):max(right_eye_y), min(right_eye_x):max(right_eye_x),:]

            T = 50

            left_eye_thresholded_index = np.stack(((left_eye_im.sum(axis=2) // 3) < T).nonzero(), axis=1)
            left_eye_cord = left_eye_thresholded_index.mean(axis = 0, dtype=np.float16)
            right_eye_thresholded_index = np.stack(((right_eye_im.sum(axis=2) // 3) < T).nonzero(), axis=1)
            right_eye_cord = right_eye_thresholded_index.mean(axis = 0, dtype=np.float16)

            def add_tuple(a, b):

                return (a[0] + b[1], a[1] + b[0])

            if not np.isnan(left_eye_cord).any():
                left_eye_cord_int = tuple(map(int, left_eye_cord))
                #print(left_eye_cord, 'int : ', left_eye_cord_int)
                memory_cord.pop()
                memory_cord.append(add_tuple(left_lefttop,left_eye_cord_int))
            if not np.isnan(right_eye_cord).any():
                right_eye_cord_int = tuple(map(int, right_eye_cord))
                memory_cord_right.pop()
                memory_cord_right.append(add_tuple(right_lefttop, right_eye_cord_int))


            cv2.circle(img=frame, center=memory_cord[-1], radius=2, color=(0, 0, 255), thickness=-1)

            cv2.circle(img=frame, center=memory_cord_right[-1], radius=2, color=(0, 0, 255), thickness=-1)

            cv2.imshow(winname="Face", mat=frame)


            if cv2.waitKey(1) == ord('q'):
                break



            # final output
            #left_center # 완쪽 눈 중심 좌표
            #right_center # 오른쪽 눈 중심 좌표
            #memory_cord[-1] # 왼쪽 검은자 중심 좌표
            #memory_cord_right[-1] # 오른쪽 검은자 중심 좌표


            ''' 학습 시킬 때 활성 화 '''
            #f = open('write.csv', 'a', newline='')
            #wr = csv.writer(f)
            #wr.writerow([((left_center[0]-memory_cord[-1][0])+(right_center[0]-memory_cord_right[-1][0]))/2,((left_center[1]-memory_cord[-1][1])+(right_center[1]-memory_cord_right[-1][1]))/2 ,0])
            test_x = ((left_center[0]-memory_cord[-1][0])+(right_center[0]-memory_cord_right[-1][0]))/2
            test_y = ((left_center[1]-memory_cord[-1][1])+(right_center[1]-memory_cord_right[-1][1]))/2


            ''' 임의로 정한 부정행위 값'''
            if abs(test_x) > 1.7 and abs(test_y) > 1.85:
                cnt = cnt + 1
                # print(main.classification.W,main.classification.b)
                if (cnt == 3):
                    print("부정행위가 감지되었습니다.")
                    cnt = 0

            ''' Classification 적용한 부정행위 진단
            test = [[test_x, test_y]]
            #print(test)
            test_data = torch.FloatTensor(test)
            W = torch.FloatTensor([[0.0897],[-0.0041]])
            #W = tf.constant([[0.0897],[-0.0041]])
            b = torch.FloatTensor([0.8373])
            #b = tf.constant([0.8373])
            main.classification.hypothesis = torch.sigmoid(test_data.matmul(W) + b)  # or .mm or @
            predict = main.classification.hypothesis >= torch.FloatTensor([0.5])
            
            if (predict == 0):
                cnt=cnt+1
                #print(main.classification.W,main.classification.b)
                if(cnt==3):
                    print("부정행위가 감지되었습니다.")
                    cnt=0
            '''

    # Close all windows
    cap.relase()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detection_cheat_for_eye()