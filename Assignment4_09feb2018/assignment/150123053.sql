create database 09feb2018;

use 09feb2018;	

-- Comments are also included in the create table command corresponding to the columns

/*
Table for course with attributes course_id and division. Primary key is (course_id,division)
because for every record the pair(course_id,division) is unique. 
the div_assign constraint enforces that divisions are assigned to institute level core courses only (100 level courses).
Divisions are NOT assigned to department level courses
*/ 

create table course (course_id char(6) not null comment 'the unique id for course', division enum('NA','I','II','III','IV') not null 
comment 'enum data type is taken for enforcing the fixed set of values. Division in Course entity take values from the set {I, II, III, IV, NA}',
constraint cid_pk primary key(course_id,division) comment 'every tuple corresponding to
(course_id,division) is unique',constraint div_assign check(((course_id not like '%101' or course_id 
not like '%102') and division = 'NA') and ((course_id like '%101' or course_id like '%102') and division <> 'NA')));

/*
Table for department with attributes department_id and name . Primary key is (department_id)
because for every record department_id is unique in the table.
*/

create table department(department_id char(4) not null, name varchar(52) not null,
constraint dep_pk primary key(department_id) comment 'every tuple corresponding to (department_id) is unique');

/* Table for slot, with attributes letter, day, start time and end time with primary key (letter,day)
because for every record the pair(letter,day) is unique. 
*/     

create table slot(letter enum('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
'I', 'J', 'K', 'L', 'A1', 'B1', 'C1', 'D1', 'E1') not null comment 'enum data type is taken for enforcing the attribute to accept a
fixed set of values',day enum('Monday','Tuesday','Wednesday','Thursday','Friday') not null comment 'enum data type is taken for enforcing the fixed set of values', start_time time, end_time time,
constraint slot_pk primary key(letter,day) comment 'every tuple corresponding to (letter,day) 
is unique');
 
/*
Table for room with attributes room_numner,location and primary key constraint
(room_number) because it is unique in each tuple 
*/

create table room(room_number char(18) not null,location enum('Core-I', 'Core-II',
'Core-III', 'Core-IV', 'LH', 'Local') not null, constraint room_pk primary key(room_number)
comment 'every tuple corresponding to (room_number) is unique');

/*
Table for scheduled_in with attributes sch_department_id,sch_course_id,sch_letter,sch_division,sch_room_number,
sch_day with primary key constraint consisting of all the attributes and foreign key constraints
referencing columns in primary key constraints in previous tables course,department,slot and room
A foreign key (FK) is a column or combination of columns that is used to establish and enforce a link between the data in two tables. 
The key constraint from entity course to relationship ScheduledIn is relaxed because there are 
multiple tuples with the same key (course_id,division) in the table , so (course_id,division) cannot
be a primary key for this table. 
Foreign Key constraint enforces referential integrity by guaranteeing that changes cannot be made to data in the primary key table if those changes invalidate the link to data in the foreign key table.
*/

create table scheduled_in(sch_department_id char(4) not null, sch_course_id char(6) not null, sch_division enum('NA','I','II','III','IV') not null,
sch_letter enum('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
'I', 'J', 'K', 'L', 'A1', 'B1', 'C1', 'D1', 'E1') not null,sch_room_number char(15) not null,sch_day enum('Monday','Tuesday','Wednesday','Thursday','Friday') not null,
constraint sch_pk primary key(sch_department_id,sch_course_id,sch_division,sch_letter,sch_room_number,sch_day)
comment 'all the fields have to be included in the primary key because there is no other 
distinguishable factor', constraint course_fk foreign key(sch_course_id,sch_division)  references
course(course_id,division) on delete cascade,constraint dep_fk foreign key(sch_department_id) 
references department(department_id) on delete cascade,
constraint slot_fk foreign key(sch_letter,sch_day) references slot(letter,day) on delete cascade, 
constraint room_fk foreign key(sch_room_number) references room(room_number) on delete cascade);

	
