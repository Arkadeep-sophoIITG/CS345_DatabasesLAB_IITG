use 150123053_23feb2018;
delimiter $$
drop procedure if exists count_credits;

# procedure declaration 
create procedure count_credits()
	begin

# varaible to store roll number of student
	declare stud_roll char(20);

# varaible to store roll number of student	
	declare stud_name varchar(60);

# temporary varaible to store roll number of student		
	declare temp_roll char(20);

#temporary count variable to store sum of credits of courses alloted to a student
	declare temp_count int;

#course id extracted from cwsl table 
	declare cid_stud char(8);

# variable to store number of credits of a course as selected from cc table
	declare no_cred smallint DEFAULT 0;
	
# conditional varaible to terminate the loop when data fetched from cursor is exhausted
	DECLARE no_more_rows INT DEFAULT 0;


# cursor declared for iterating through each record of cwsl table where records are grouped by roll number
	declare cur_stud cursor for select distinct roll_number,name,cid from cwsl order by roll_number;
	
	/*
	Shorthand for the class of SQLSTATE values that begin with '02'. 
	This is relevant within the context of cursors and is used to control what happens when a cursor reaches the end of a data set.
	If no more rows are available, a No Data condition occurs with SQLSTATE value '02000'.
	To detect this condition, a handler is set up for it or for a NOT FOUND condition.
	*/

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET no_more_rows = 1;
	drop table if exists bondcredit;
	
# temporary table to store the results of the query in procedure

	create temporary table bondcredit (roll_number char(20) NOT NULL,name varchar(60) NOT NULL, credits int not null);
	open cur_stud;

	# fetching roll,name and cid from cursor
	fetch cur_stud into stud_roll,stud_name,cid_stud;

# external loop to go through each record of cwsl table

	external_loop: loop
	# setting stud_roll and temp_roll equal to loop through a particular student's courses
		set temp_roll=stud_roll;

		# resetting the course credits counter
		set temp_count =0;	

		set no_cred = 0;
		
		# using a while loop to iterate through a particular student's courses
		studloop:while (strcmp(temp_roll,stud_roll)=0) do
		
		# selecting the number of credits of course cid_stud from cc table
			set no_cred = (select number_of_credits from cc where course_id = cid_stud);

			# aggregating credits of courses alloted to a student
			set temp_count = temp_count + no_cred;
			
			# if creditsum is greater than 40 then insert into result table the student details
			if (temp_count > 40 )then 
				insert into bondcredit values(stud_roll,stud_name,temp_count);
				leave studloop;
			end if;
			
			# fetching next record from cwsl to check for creditsum
			fetch cur_stud into stud_roll,stud_name,cid_stud;

		# if data is exhausted then loop is terminated
	
			if no_more_rows =1 then
				leave external_loop;
			end if;
		end while studloop;


	end loop external_loop;

	# printing the results
	select *from bondcredit;
	close cur_stud;
end$$
delimiter ;

# calling the procedure
call count_credits();
