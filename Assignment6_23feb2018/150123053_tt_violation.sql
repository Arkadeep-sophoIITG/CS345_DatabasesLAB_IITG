use 150123053_23feb2018;
delimiter $$

drop procedure if exists tt_violation;

#procedure declaration
create procedure `tt_violation`()
begin

# varaible to store roll number of student
declare stud_roll char(20);

# varaible to store name of student
declare stud_name varchar(60);

# variable to store the course_id with which comparison is to be made
declare cid1_stud char(8);

#variable to store exam_date, start_time and end_time.
declare exam_stud_date date;
declare start_stud_time time;
declare end_stud_time time;

# conditional varaible to terminate the outer loop when data fetched from outer cursor is exhausted
DECLARE no_more_rows INT DEFAULT 0;

# cursor declared for iterating through each record of cwsl table
declare cur_cwsl cursor for select distinct roll_number,name,cid from cwsl ;

/*
 Shorthand for the class of SQLSTATE values that begin with '02'. 
This is relevant within the context of cursors and is used to control what happens when a cursor reaches the end of a data set.
If no more rows are available, a No Data condition occurs with SQLSTATE value '02000'.
To detect this condition, a handler is set up for it or for a NOT FOUND condition.
*/

DECLARE CONTINUE HANDLER FOR NOT FOUND SET no_more_rows = 1;

drop table if exists violation;

# temporary table to store the results of the query in procedure

create temporary table violation(roll_number char(20) NOT NULL,name varchar(60) NOT NULL, 
cid1 char(8) not null,cid2 char(8) not null);


open cur_cwsl;

# loop to go through each record in cwsl table
cwsl_loop:loop
	# student roll,name and alloted course is fetched from cursor
	fetch cur_cwsl into stud_roll,stud_name,cid1_stud;
	
	# select statements for finding the date and start time and end time of the course from ett table
	set exam_stud_date = (select exam_date from ett where course_id = cid1_stud order by line_number desc limit 1 );
	set start_stud_time = (select start_time from ett where course_id=cid1_stud order by line_number desc limit 1);
		
	# definition of a block to support nested cursor
		nestblock:begin


			declare cid2_stud char(8);

# conditional varaible to terminate the inner loop when data fetched from nested cursor is exhausted
			declare no_more_rows_comp int DEFAULT 0;
			declare exam_comp_date date;
			declare start_comp_time time;
			declare end_comp_time time;
			
			/*
			select statement for selecting those courses from cwsl which are alloted to the same 
			roll number from above cursor (stud_roll) and having course_id other than that have already been compared  
			*/
			declare comp_cwsl cursor for select distinct cid from cwsl where roll_number=stud_roll and cid > cid1_stud;
			
			# as before a continue handler is declared for terminating the loop when no data is found
			
			DECLARE CONTINUE HANDLER FOR NOT FOUND SET no_more_rows_comp = 1;
			open comp_cwsl;

			comp_cwsl_loop:loop
				fetch comp_cwsl into cid2_stud;
				
				# if data is exhausted the loop is terminated
				if (no_more_rows_comp =1) then
					close comp_cwsl;
					leave comp_cwsl_loop;
					set no_more_rows=0;
				end if;

				# selecting date and start time of the courses to be compared with cid1_stud

				set exam_comp_date = (select exam_date from ett where course_id = cid2_stud order by line_number desc limit 1);
				set start_comp_time = (select start_time from ett where course_id=cid2_stud order by line_number desc limit 1);
				
				/* checking if there is a overlap between the exam timetables of cid1_stud and cid2_stud
				if condition is satisfied then it is added to the result table */
				
				if (cid1_stud <> cid2_stud and exam_comp_date = exam_stud_date and start_comp_time=start_stud_time) then 	
						insert into violation values(stud_roll,stud_name,cid1_stud,cid2_stud);
				end if;

			# continuously printing the result table
			-- select * from violation;

			# end of loop comp_cwsl_loop
			end loop comp_cwsl_loop;

		# end of nestblock
		end nestblock;

	# if data is exhausted then loop is terminated

	if (no_more_rows=1) then
		close cur_cwsl;
		leave cwsl_loop;
	end if;
end loop cwsl_loop;

select * from violation;

end$$

delimiter ;

# calling the procedure
call tt_violation();



			  

