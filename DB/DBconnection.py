import numpy as np
import datetime
import pymysql


#mysql 연결
conn = pymysql.connect(
    host = 'localhost', 
    user ='Sejong', 
    password = 'sejong2020H', 
    db = 'exam',
    charset = 'utf8'
)

#DB에 참조하기 위한 객체
curs = conn.cursor(pymysql.cursors.DictCursor) 
#curs = conn.cursor() 

# 학생 이미지 select
def load_studentdata(exam_id):
    sql = "select ES.student_id, I.file from EXAM_STUDENT ES inner join IMAGE I on ES.student_id = I.student_id where ES.exam_id = %s" 
    curs.execute(sql, exam_id)
    conn.commit()
    return curs.fetchall()

# 클립보드 내용 저장
def store_clipboard(exam_id, student_id, clipboard):
    sql = "update EXAM_STUDENT set clipboard=%s where exam_id = %s and student_id = %s"
    curs.execute(sql, (clipboard, exam_id, student_id))
    conn.commit()
    
# 부정행위 시 face_log 기록 저장
def store_facelog(exam_id, student_id, image, error_type, remarks):
    sql = "insert into FACE_LOG (exam_id, student_id, time, error_type, image, remarks) values (%s, %s, now(), %s, %s, %s)"
    curs.execute(sql, (exam_id, student_id, error_type, image, remarks))
    conn.commit()

# data = load_studentdata(2)
# print(data)

# store_clipboard(1, 18011529, "어쩌구저쩌구")

# store_facelog(5, 18011529, "log_images/image1.jpg", 2, "three")