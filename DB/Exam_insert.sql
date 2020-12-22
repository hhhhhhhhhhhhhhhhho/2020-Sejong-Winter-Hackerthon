
insert into EXAM values (1, "미분적분학", "2020-12-22 13:00:00", "2020-12-22 15:00:00");
insert into EXAM values (2, "선형대수및프로그래밍", "2020-12-22 13:30:00", "2020-12-22 15:30:00");
insert into EXAM values (3, "C프로그래밍", "2020-12-21 13:00:00", "2020-12-21 15:00:00");
insert into EXAM values (4, "Python", "2020-12-21 10:00:00", "2020-12-21 11:00:00");
insert into EXAM values (5, "알고리즘", "2020-12-23 16:00:00", "2020-12-22 16:30:00");

insert into STUDENT values (18011529, "김효경");
insert into STUDENT values (18011549, "박태정");
insert into STUDENT values (17011502, "김찬규");
insert into STUDENT values (17011477, "목승주");
insert into STUDENT values (20000000, "강동원");
insert into STUDENT values (19022222, "배수지");
insert into STUDENT values (16033333, "남주혁");
insert into STUDENT values (15044444, "서현진");
insert into STUDENT values (18055555, "유재석");
insert into STUDENT values (17012121, "조이");
insert into STUDENT values (14054545, "이재욱");

insert into EXAM_STUDENT values (1, 18011529, "");
insert into EXAM_STUDENT values (1, 20000000, "");
insert into EXAM_STUDENT values (1, 19022222, "");
insert into EXAM_STUDENT values (1, 15044444, "");
insert into EXAM_STUDENT values (1, 14054545, "");

insert into EXAM_STUDENT values (2, 18011529, "");
insert into EXAM_STUDENT values (2, 18011549, "");
insert into EXAM_STUDENT values (2, 17011502, "");
insert into EXAM_STUDENT values (2, 17011477, "");
insert into EXAM_STUDENT values (2, 19022222, "");

insert into EXAM_STUDENT values (3, 18011529, "");
insert into EXAM_STUDENT values (3, 17011477, "");
insert into EXAM_STUDENT values (3, 20000000, "");
insert into EXAM_STUDENT values (3, 16033333, "");
insert into EXAM_STUDENT values (3, 17012121, "");

insert into EXAM_STUDENT values (4, 18011529, "");
insert into EXAM_STUDENT values (4, 18011549, "");
insert into EXAM_STUDENT values (4, 17011502, "");
insert into EXAM_STUDENT values (4, 15044444, "");
insert into EXAM_STUDENT values (4, 18055555, "");

insert into EXAM_STUDENT values (5, 18011529, "");
insert into EXAM_STUDENT values (5, 18011549, "");
insert into EXAM_STUDENT values (5, 20000000, "");
insert into EXAM_STUDENT values (5, 18055555, "");
insert into EXAM_STUDENT values (5, 14054545, "");

insert into IMAGE values (1, 18011529, "H:/2020Hackathon/team/2020-Sejong-Winter-Hackerthon/DB/Server/person_images/test.jpg");

insert into IMAGE values (2, 18011549, "H:/2020Hackathon/team/2020-Sejong-Winter-Hackerthon/DB/Server/person_images/park.jpg");

insert into IMAGE values (3, 17011502, "H:/2020Hackathon/team/2020-Sejong-Winter-Hackerthon/DB/Server/person_images/kim.jpg");

insert into IMAGE values (4, 17011477, "H:/2020Hackathon/team/2020-Sejong-Winter-Hackerthon/DB/Server/person_images/mok.jpg");

insert into IMAGE values (5, 20000000, "images/20000000_1.jpg");

insert into IMAGE values (6, 19022222, "images/19022222_1.jpg");


insert into IMAGE values (7, 16033333, "images/16033333_1.jpg");

insert into IMAGE values (8, 15044444, "images/15044444_1.jpg");

insert into IMAGE values (9, 18055555, "images/18055555_1.jpg");

insert into IMAGE values (10, 17012121, "images/17012121_1.jpg");

insert into IMAGE values (11, 14054545, "images/14054545_1.jpg");

insert into FACE_LOG (exam_id, student_id, time, error_type, image, remarks) values (1, 18011529, now(), 1, "log_image/image_1.jpg", "5sec");
insert into FACE_LOG (exam_id, student_id, time, error_type, image, remarks) values (3, 18011529, now(), 2, "log_image/image_2.jpg", "two people");
insert into FACE_LOG (exam_id, student_id, time, error_type, image, remarks) values (4, 19022222, now(), 3, "log_image/image_3.jpg", "different person");
insert into FACE_LOG (exam_id, student_id, time, error_type, image, remarks) values (5, 18055555, now(), 1, "log_image/image_4.jpg", "5sec");
insert into FACE_LOG (exam_id, student_id, time, error_type, image, remarks) values (3, 17012121, now(), 1, "log_image/image_5.jpg", "4sec");