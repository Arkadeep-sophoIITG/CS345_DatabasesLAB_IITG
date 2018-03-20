#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

typedef unsigned long long ll;

typedef struct student_record
{
    char name[200];
    char roll[200];
    char exam_courses[800][100];
    int creditsum;
    int courseNo;
    // struct student_record *next;

}student_record;

typedef struct course_credits{
    char course_name[100];
    int credits;
}course_credits;

typedef struct course_time_table{
    char course_name[200];
    char date[200];
    char start[200];
    char end[200];
}course_time_table;

// typedef struct record_list
// {
//     student_record *head,*tail;
//     int size;
// }record_list;

// student_record *init_stud_info(student_record *node,char *name,char *roll,char *exam_courses)
// {
//     node =(student_record *)malloc(sizeof(student_record));
//     node->name = (char *)malloc(sizeof(char));
//     strcpy(node->name,name);
//     node->roll = (char *)malloc(sizeof(char));
//     strcpy(node->roll,roll);
//     node->exam_courses[node->no_exam_courses] = (char *)malloc(sizeof(char));
//     strcpy(node->exam_courses[node->no_exam_courses],exam_courses);
//     return node;
// }

// //initialize student list of structures
// record_list *init_record_list(record_list *record)
// {
//     record = (record_list *)malloc(sizeof(record_list));
//     record->head = NULL;
//     record->tail = NULL;
//     return record;
// }

char *concat(char *s1, const char *s2)
{
    char *result = malloc(strlen(s1)+strlen(s2)+1);//+1 for the null-terminator
    //in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

void removeSubstring(char *s,const char *toremove)
{
  while( s=strstr(s,toremove) )
    memmove(s,s+strlen(toremove),1+strlen(s+strlen(toremove)));
}
// //inserting record from file
// void insert(record_list *record,char *name,char *roll,char *exam_courses)
// {
//     if (record->head == NULL)
//     {
//         student_record *new_node;
//         new_node->no_exam_courses = 0;
//         new_node->creditsum = 0;
//         new_node =init_stud_info(new_node,name,roll,exam_courses);
//         record->head = new_node;
//         record->tail = new_node;
//     }
//     else
//     {
//         student_record *temp = record->head;
//         while(temp->next != NULL && strcmp(temp->roll,roll)!=0)
//         {
//             temp=temp->next;
//         }
//         if(temp->next == NULL)
//         {
//         student_record *new_node;
//         new_node->no_exam_courses = 0;
//         new_node->creditsum = 0;
//         new_node = init_stud_info(new_node,name,roll,exam_courses);
//         temp->next = new_node;
//         record->tail=new_node;
//         // printf("%s\n",new_node->name);
//         }
//         if(temp->next != NULL)
//         {
//             ++temp->no_exam_courses;
//             temp->exam_courses[temp->no_exam_courses]=(char *)malloc(sizeof(char));
//             strcpy(temp->exam_courses[temp->no_exam_courses],exam_courses);

//         }
//     }
//     ++record->size;
// }

// record_list *record;
struct student_record records[5000];
struct course_credits cred[1000];
struct course_time_table table[1000];
int main (int c, char **v) {
    // record = init_record_list(record);
    int len;
    struct dirent *pDirent;
    DIR *pDir,*pDir2,*pDir3,*pDir4;
    FILE **fp1;
    char **fileNames;
    unsigned long long roll;
    char held[100],status[20],damn[100];
    int no=0;
    if (c < 2) {
        printf ("Usage: testprog <dirname>\n");
        return 1;
    }
    pDir = opendir (v[1]);
    if (pDir == NULL) {
        printf ("Cannot open directory '%s'\n", v[1]);
        return 1;
    }

    while ((pDirent = readdir(pDir)) != NULL) {
        if((strcmp(pDirent->d_name,".")==0 || strcmp(pDirent->d_name,"..")==0 || (*pDirent->d_name) == '.' ))
            {
            }
        else
        {
            if(strstr(pDirent->d_name,"csv"))
            {
            ++no;
        }
    }
    }
    int i=0;
    pDir2 = opendir(v[1]);  
    fileNames = (char **)malloc(sizeof(char *)*no);
    char *coursenames[12];
    while ((pDirent = readdir(pDir2)) != NULL) {
        if((strcmp(pDirent->d_name,".")==0 || strcmp(pDirent->d_name,"..")==0 || (*pDirent->d_name) == '.' ))
            {
            }
        else
        {
            if(strstr(pDirent->d_name,"csv"))
            {
            char *str = pDirent->d_name;
            fileNames[i]=(char *)malloc(sizeof(char));
            str = concat(v[1],str);
            strcpy(fileNames[i],str);
            i++;
        }
        }

    }

    char *path = "database-19-jan-2018/course-wise-students-list/";
    pDir3 = opendir(path);
    int count =0;
        while ((pDirent = readdir(pDir3)) != NULL) {
        if((strcmp(pDirent->d_name,".")==0 || strcmp(pDirent->d_name,"..")==0 || (*pDirent->d_name) == '.' ))
            {
            }
        else
        {
            char *str = pDirent->d_name;
            coursenames[count]=(char *)malloc(sizeof(char));
            str = concat(path,str);
            strcpy(coursenames[count],str);
            ++count;
        
        }

    }
    int k=0;
     ll f=0;
     int countt =0;
    for(k=0;k<11;k++)
    {
        int serial;char roll_no[50]; char name[200];char email[200];
        pDir4 = opendir(coursenames[k]);
        FILE *fp_courses;
        while ((pDirent = readdir(pDir4)) != NULL) {
        if((strcmp(pDirent->d_name,".")==0 || strcmp(pDirent->d_name,"..")==0 || (*pDirent->d_name) == '.' ))
            {
            }
        else
        {
            char *str;
            str =(char *)malloc(sizeof(char));
            char *course;
            course = (char *)malloc(sizeof(char));
            strcpy(str,pDirent->d_name);
            strcpy(course,str);
            char cd[100];
            int lo=0;
            while(*course!='.'){
                cd[lo]=*course;
                lo++;
                course=course+1;
            }
            cd[lo]='\0';
            // printf("%s\n",cd);                                                                                                                                                                                     
            str = concat("/",str);
            str = concat(coursenames[k],str);
            fp_courses = fopen(str,"r");
            while(true)
            {
            int ret = fscanf(fp_courses,"%d,%[^,],%[^,],%[^\n]",&serial,roll_no,name,email); //reading from file
            if(ret < 3)
            {
                break;
            }

            if (countt == 0)
            {
                strcpy(records[countt].name,name);
                strcpy(records[countt].roll,roll_no);
                records[countt].creditsum = 0;
                records[countt].courseNo = 0;
                int r;
                r = records[countt].courseNo;
                strcpy(records[countt].exam_courses[r],cd);
                ++records[countt].courseNo;
                ++countt;
            }
            else
            {
                int op=0;
                bool found =false;
                while(op<=countt)
                {
                    if (strcmp(records[op].roll,roll_no)==0)
                    {
                        strcpy(records[op].exam_courses[records[op].courseNo],cd);
                        ++records[op].courseNo;
                        found =true;
                    }
                    ++op;
                }
                if (!found)
                {
                    strcpy(records[countt].name,name);
                    strcpy(records[countt].roll,roll_no);
                    records[countt].creditsum = 0;
                    records[countt].courseNo = 0;
                    strcpy(records[countt].exam_courses[records[countt].courseNo],cd);
                    ++records[countt].courseNo;
                    ++countt;
                }
            
            }

            
        }
            free(str);


        }

}
}


    int opi=0,tp=0,cxzx=0;
    // for(opi=0;opi<countt;opi++)
    // {
    //     printf("%s\n",records[opi].name);
    //     for( tp=0;tp<records[opi].courseNo;tp++)
    //     {
    //         printf("%s\n",records[opi].exam_courses[tp]);
    //     }
    // }
    FILE *fp3;
    char course_name[200];
    int credit;
    fp3 = fopen("database-19-jan-2018/course-credits.csv","r");

    int ko=0;

    FILE *fp6;
    fp6=fopen("course-credits_great40.csv","w");
    while(true)
    {
       int ret = fscanf(fp3,"%[^,],%d\n",course_name,&credit); //reading from file
            if(ret !=2 )
            {
                break;
            }
        // printf("%s %d\n",course_name,credit);
        strcpy(cred[ko].course_name,course_name);
        // printf("struct course: %s\n",cred[ko].course_name);
        cred[ko].credits=credit;
        ++ko;
    }
    int fir=0,sec=0,third=0;
    int summ=0;    
    int studs=0;
    for(fir=0;fir<countt;fir++)
    {
        summ=0;
        for(sec=0;sec<ko;sec++)
        {
            for(third=0;third<=records[fir].courseNo;third++)
            {
                if(strcmp(cred[sec].course_name,records[fir].exam_courses[third])==0)
                {
                    summ=summ+cred[sec].credits;
                }
            }
        }
        if(summ > 40)
        {
            fprintf(fp6, "%s,%s,%d\n",records[fir].roll,records[fir].name,summ );
        }
    }

    FILE *fp4 =fopen("./database-19-jan-2018/exam-time-table.csv","r");
    char name_course[200],date[200],start[200],end[200];

    // if(!fp4) return;

    // printf("yo");
    int rob=0;
    int ui=0;
    bool fnd=false;
    while(true)
    {
       int ret = fscanf(fp4,"%[^,],%[^,],%[^,],%[^\n]\n",name_course,date,start,end); //reading from file
            if(ret !=4 )
            {
                break;
            }

        fnd = false;

        for(ui=0;ui<rob;ui++)
        {
            if(strcmp(table[ui].course_name,name_course)==0 && strcmp(table[ui].date,date)==0 && strcmp(table[ui].start,start)==0 && strcmp(table[ui].end,end)==0)
            {
                fnd =true;
            }

        }
        if (!fnd)
        {
            strcpy(table[rob].course_name,name_course);
            strcpy(table[rob].date,date);
            strcpy(table[rob].start,start);
            strcpy(table[rob].end,end);
            ++rob;
        }
    }

    int f1=0,s1=0,t1=0,pit=0,kit=0;
    int fnd2;
    FILE *fp8;
    fp8 =fopen("exam-time-table_clash.csv","w");
    for(f1=0;f1<countt;f1++)
    {
        for(s1 =0;s1<records[f1].courseNo-1;s1++)
        {
            for(t1=s1+1;t1<records[f1].courseNo;t1++)
            {
                fnd2=1;
                for(pit=0;pit<rob;pit++)
                {
                    if(strcmp(table[pit].course_name,records[f1].exam_courses[s1])!=0)

                    {
                        continue;
                    }
                    for(kit=0;kit<rob;kit++)
                    {

                    if(strcmp(table[kit].course_name,records[f1].exam_courses[t1])!=0)
                        continue;
                    if(strcmp(table[pit].date,table[kit].date)==0 && strcmp(table[pit].start,table[kit].start)==0)
                    {
                        fnd2=0;
                        break;
                    }
                    

                    }
                    if(fnd2==0){
                    break;
                    }


                }

                if(fnd2==0){
                    fprintf(fp8,"%s,%s,%s,%s \n",records[f1].roll,records[f1].name,records[f1].exam_courses[s1],records[f1].exam_courses[t1]);
                }
            }
        }
    }
    closedir (pDir);
    return 0;
}
