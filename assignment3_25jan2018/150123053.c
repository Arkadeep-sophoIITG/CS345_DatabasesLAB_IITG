#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

typedef unsigned long long ll;

char *concat(char *s1, const char *s2)
{
    char *result = malloc(strlen(s1)+strlen(s2)+1);//+1 for the null-terminator
    //in real code you would check for errors in malloc here
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

int main(int c,char **v)
{

FILE *fp3;
    char course_name[200];
    int credit;
    fp3 = fopen("database-19-jan-2018/course-credits.csv","r");
FILE *fp4 =fopen("database-19-jan-2018/exam-time-table.csv","r");
FILE *fp_w1=fopen("150123053_ett.sql","w");
FILE *fp_w2 = fopen("150123053_cc.sql","w");
    char name_course[200],date[200],start[200],end[200];
    if (c < 2) {
        printf ("Usage: testprog <dirname>\n");
        return 1;
    }
    if(!fp4) return;
    while(true)
    {
       int ret1 = fscanf(fp4,"%[^,],%[^,],%[^,],%[^\n]\n",name_course,date,start,end); //reading from file
            if(ret1 !=4 )
            {
                break;
            }    

        fprintf(fp_w1, "INSERT INTO ett values('%s','%s','%s','%s');\n",name_course,date,start,end);
        fprintf(fp_w1, "INSERT INTO ett_temp  values('%s','%s','%s','%s');\n",name_course,date,start,end);
        fprintf(fp_w1, "INSERT INTO ett_clone values('%s','%s','%s','%s');\n",name_course,date,start,end);

    }

    while(true)
    {
       int ret = fscanf(fp3,"%[^,],%d\n",course_name,&credit); //reading from file
            if(ret !=2 )
            {
                break;
            }
     fprintf(fp_w2, "INSERT INTO cc values ('%s',%d);\n",course_name,credit);
     fprintf(fp_w2, "INSERT INTO cc_temp values ('%s', %d);\n",course_name,credit);
     fprintf(fp_w2, "INSERT INTO cc_clone values ('%s', %d);\n",course_name,credit);
    }

FILE *fp_w3 = fopen("150123053_cwsl.sql","w");
int len;
    struct dirent *pDirent;
    DIR *pDir,*pDir2,*pDir3,*pDir4;
    FILE **fp1;
    char **fileNames;
    unsigned long long roll;
    char held[100],status[20],damn[100];
    int no=0;
    pDir = opendir (v[1]);
    if (pDir == NULL) {
        printf ("Cannot open directory ");
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
            fprintf(fp_w3, "INSERT INTO cwsl values('%s',%d,'%s','%s','%s');\n",cd,serial,roll_no,name,email);     
            fprintf(fp_w3, "INSERT INTO cwsl_temp values('%s',%d,'%s','%s','%s');\n",cd,serial,roll_no,name,email);     
             fprintf(fp_w3, "INSERT INTO cwsl_clone values('%s',%d,'%s','%s','%s');\n",cd,serial,roll_no,name,email);     


        }
            free(str);


        }
    }
}
return 0;
}





    