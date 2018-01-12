#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

//student structure
typedef struct student
{
	unsigned long long roll;
	char *held_on;
	char *status;
	struct student *next;
}student;

//student list of structures
typedef struct stud_list
{
	student *head,*tail;
	int size;
}stud_list;

//initialize student structure
student *init_stud_info(student *node,unsigned long long roll,char *held_on,char *status)
{
	node =(student *)malloc(sizeof(student));
	node->roll = roll;
	node->held_on = (char *)malloc(sizeof(char));
	strcpy(node->held_on,held_on);
	node->status = (char *)malloc(sizeof(char));
	strcpy(node->status,status);
	return node;
}

//initialize student list of structures
stud_list *init_stud_list(stud_list *stud)
{
	stud = (stud_list *)malloc(sizeof(stud_list));
	stud->head = NULL;
	stud->tail = NULL;
	return stud;
}

//inserting record from file
void insert(stud_list *stud,unsigned long long roll,char *held_on,char *status)
{
	if (stud->head == NULL)
	{
		student *new_node;
		new_node =init_stud_info(new_node,roll,held_on,status);
		stud->head = new_node;
		stud->tail = new_node;
	}
	else
	{
		student *temp = stud->head;
		while(temp->next!=NULL)
		{
			temp=temp->next;
		}
		student *new_node;
		new_node = init_stud_info(new_node,roll,held_on,status);
		temp->next = new_node;
		stud->tail=new_node;
	}
	++stud->size;
}

// Function to print the list of students (according to percentage) Part (b)
void search (stud_list *stud)
{
	student *temp = stud->head;
	long long int roll_no = temp->roll;
	float present,total;
	present=total=0;
	student *prev;
	FILE *fp3 = fopen("L75.csv","w");
	FILE *fp4 = fopen("G75.csv","w");
	while (temp->next!=NULL)
	{
	present=total=0;
	roll_no=temp->roll;
	while(temp->roll==roll_no && temp->next!=NULL)
	{
		if(strcmp(temp->status,"Present")==0)
		{
			++present;
		}
		++total;
		prev =temp;
		temp = temp->next;
	}
	float per=(present*100)/total;
	if (per < 75)          //Checks list of students with less than 75%
	{
		fseek(fp3,0,SEEK_END);
		fprintf(fp3, "%llu  %d  %f \n",prev->roll,(int)present,per);
	}
	if (per >= 75)			//Checks list of students with greater than equal to 75%
	{
		fseek(fp4,0,SEEK_END);
		fprintf(fp4, "%llu  %d  %f \n",prev->roll,(int)present,per);
	}

}
}

//Function to print the whole data through linked list data structure
void print_all(stud_list *stud)
{
	student *temp = stud->head;
	while(temp!=NULL)
	{
		printf("%llu  %s  %s\n",temp->roll,temp->held_on,temp->status);
		temp = temp->next;
	}
}

stud_list *stud;
int main(void)
{
	FILE *fp1;
	unsigned long long roll;
	stud = init_stud_list(stud);
	char held[100],status[20];
	fp1 = fopen("database_12jan2017.csv","r");
	if (fp1 == NULL)
	{
		printf("%s\n","File not found");
	}
	
	else
	{
		while(true)
		{
			int ret = fscanf(fp1,"%llu,%[^,],%s",&roll,held,status); //reading from file
			if(ret == EOF)
			{
				break;
			}
			insert(stud,roll,held,status);  //inserting into stud_list
		}
	}
	print_all(stud);  //printing the whole data on console
	search(stud);	  //part (b)
}

