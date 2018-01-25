create database 25jan2018;
use 25jan2018;

#course_id is stored as char because it is within a fixed length
create table ett (course_id char(8) NOT NULL, exam_date DATE NOT NULL , start_time char(20) NOT NULL, end_time char(20) NOT NULL, primary key(course_id,exam_date,start_time,end_time));


create table cc  (course_id char(8) NOT NULL , number_of_credits SMALLINT NOT NULL, primary key(course_id));
#primary key is course_id because it is unique and uniquely identifies each field;


#primary_key is (cid,roll_no) because they uniquely identifies each field; 
create table cwsl (cid char(8) NOT NULL, serial_number INT , roll_number varchar(30) NOT NULL, name varchar(255) NOT NULL, email varchar(255), primary key(cid,roll_number));

create table ett_temp(course_id char(8) NOT NULL, exam_date DATE NOT NULL , start_time char(20) NOT NULL, end_time char(20) NOT NULL, primary key(course_id,exam_date,start_time,end_time));

create table cc_temp(course_id char(8) NOT NULL , number_of_credits SMALLINT NOT NULL, primary key(course_id));

create table cwsl_temp(cid char(8) NOT NULL, serial_number INT , roll_number varchar(30) NOT NULL, name varchar(255) NOT NULL, email varchar(255), primary key(cid,roll_number));

CREATE TABLE ett_clone AS SELECT * FROM ett;

CREATE TABLE cc_clone AS SELECT * FROM cc;

CREATE TABLE cwsl_clone AS SELECT * FROM cwsl;


