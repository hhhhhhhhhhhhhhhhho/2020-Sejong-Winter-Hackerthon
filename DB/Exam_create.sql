DROP DATABASE IF EXISTS  exam;
DROP USER IF EXISTS  Sejong@localhost;
create user Sejong@localhost identified WITH mysql_native_password  by 'sejong2020H';
create database exam;
grant all privileges on exam.* to Sejong@localhost with grant option;
commit;

USE exam;

CREATE TABLE EXAM (
  id INTEGER PRIMARY KEY,
  subject_name VARCHAR(20),
  start_date DATETIME,
  end_date DATETIME
);

CREATE TABLE STUDENT (
  id INTEGER PRIMARY KEY,
  name VARCHAR(20)
);

CREATE TABLE EXAM_STUDENT (
 exam_id INTEGER,
 student_id INTEGER,
 clipboard VARCHAR(255),
 PRIMARY KEY (exam_id, student_id),
 FOREIGN KEY (exam_id) REFERENCES EXAM(id),
 FOREIGN KEY (student_id) REFERENCES STUDENT(id)
);

CREATE TABLE IMAGE (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  file VARCHAR(255),
  FOREIGN KEY (student_id) REFERENCES STUDENT(id)
);

CREATE TABLE FACE_LOG (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  exam_id INTEGER,
  student_id INTEGER,
  time DATETIME,
  error_type INTEGER,
  image VARCHAR(255),
  remarks VARCHAR(20),
  FOREIGN KEY (exam_id) REFERENCES EXAM(id),
  FOREIGN KEY (student_id) REFERENCES STUDENT(id)
);




commit;