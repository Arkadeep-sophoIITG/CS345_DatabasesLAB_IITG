
use 09feb2018;

-- a)Find course ids which are in the room 2001.

select distinct sch.sch_course_id 
from scheduled_in sch
where sch.sch_room_number = '2001';

-- b) Find course ids which are in Slot C.

select distinct sch.sch_course_id
from scheduled_in sch
where sch_letter = 'C';

-- c) Find division which is allotted to room L2 or L3

select distinct sch.sch_division
from scheduled_in sch
where sch_room_number = 'L2' or sch_room_number ='L3';

-- d) Find course ids which are allotted to multiple rooms (irrespective of division)

create view multi_course
as select  distinct sch.sch_course_id,sch.sch_room_number from scheduled_in sch,room r natural join room 
where r.room_number=sch.sch_room_number order by sch.sch_course_id;

SELECT sch.sch_course_id,count(*)
FROM multi_course sch
GROUP BY sch.sch_course_id
HAVING COUNT(*) > 1;

-- e) Find department names in which any of the course of the department have
-- been allotted to room L1 or L2 or L3 or L4.

select d.name
from department d
where d.department_id in(
select sch.sch_department_id 
from scheduled_in sch
where sch.sch_room_number in ('L1','L2','L3','L4')
group by sch.sch_department_id,sch.sch_room_number);


-- f) Find department names which do not use L1 or L2 rooms.

select d.name
from department d
where d.department_id not in (
select sch.sch_department_id 
from  scheduled_in sch
where sch.sch_room_number in ('L1','L2')
group by sch.sch_department_id,sch.sch_room_number);

-- g) Find department names which have utilized all the slots.

select d.name
from department d
where d.department_id in (
select sch.sch_department_id 
from  scheduled_in sch
group by sch.sch_department_id, sch.sch_letter
having count(distinct sch_letter) = 17);

-- h) List the slots and number of courses the slot was assigned in ascending order.

select sch.sch_letter,count(distinct sch.sch_course_id)
from scheduled_in sch
group by sch.sch_letter
order by count(distinct sch.sch_course_id) asc;

-- i) List the rooms and number of courses the room was assigned in descending order.

select sch.sch_room_number,count(distinct sch.sch_course_id)
from scheduled_in sch
group by sch.sch_room_number
order by count(distinct sch.sch_course_id) desc;

-- j) Find the slot name which was assigned minimum number of courses.

create view multi_coursin
as select  distinct sch.sch_letter,sch.sch_course_id from scheduled_in sch,slot s natural join slot
where s.letter=sch.sch_letter ;

create view counts as
SELECT count(*) as num , sch.sch_letter
FROM multi_coursin sch
GROUP BY sch.sch_letter;

SELECT sch.sch_letter
FROM counts sch
WHERE sch.num =  ( SELECT MIN(sch.num) FROM counts sch);


-- k)List all the slots which were assigned to minor courses.


select distinct sch.sch_letter,sch.sch_day 
from scheduled_in sch
where sch.sch_course_id like '%M';

-- l) Department name wise list the slots which were not used.

create view multi_depslot
as select distinct sch.sch_department_id,sch.sch_letter from scheduled_in sch,slot s,department d natural join slot
where s.letter=sch.sch_letter order by sch.sch_department_id;

create view total_depslot
as select distinct d.name,d.department_id,s.letter from department d,slot s natural join slot order by d.department_id,d.name;

select td.name,td.letter from total_depslot td where (td.department_id,td.letter)  not in (select md.sch_department_id,
md.sch_letter from multi_depslot md);





