#include "types.h"
#include "stat.h"
#include "user.h"


char buf[512];
int
stricmp(char str1[], char str2[]){
   if(strlen(str1) != strlen(str2)){
     return -1;
   }
   if(strcmp(str1, str2)== 0){
     return 0;
   }
   int i,result = 0;
   for(i = 0; i <= strlen(str1); i++){
     if(((int)str1[i] == (int)str2[i]+32)||((int)str2[i] == (int)str1[i]+32)||(str1[i]== str2[i] )){
       continue;
     }
    else{
       result = -1;
   } 
   }
   return result;
}
  

void
uniq(int fd, int flag1, int flag2, int flag3)
{
    int n, i, n_line = 0;
    int counter = 1;
    char toCompare[512];
    while ((n = read(fd, &buf[i], 1)) == 1) {
      if (buf[i] == '\n') {
          buf[i] = 0;
           if (n_line == 0){
             strcpy(toCompare,buf);
           }
           else{
              if (((flag1 == 0)&&(strcmp(buf, toCompare)!= 0))||(stricmp(buf, toCompare)!= 0)){
                if(flag2 == 1){
                  printf(1, "%d\t",counter);
                }
                if((flag3 == 0) || (counter > 1)){
                  printf(1,"%s\n",toCompare);
                }
                strcpy(toCompare,buf);
                counter = 1;

              }
              else{
                 counter += 1;
              }
          }
          n_line +=1 ;
          i = 0;
          continue;
      }
      i++;


  }

  if (flag3 == 0){
    if(flag2 == 1){
      printf(1, "%d\t",counter);
    }
    printf(1, "%s\n",buf);


  }

  if(n < 0){
    printf(1, "uniq: read error\n");
  }
  exit();

}


int
main(int argc, char *argv[])
{

  char flag1[3] = "-i";
  char flag2[3] = "-c";
  char flag3[3] = "-d";
  int fd;

  if(argc == 1){
    uniq(0,0,0,0);
    exit();
  }

if((fd = open(argv[argc-1], 0)) < 0){
    printf(1, "uniq: cannot open %s\n", argv[argc-1]);
   
  }

  else{

    if(argc == 2){
      uniq(fd,0,0,0);

     }

   if(argc == 3){

      if(strcmp(argv[1],flag1) == 0){

      uniq(fd,1,0,0);
    }
    if(strcmp(argv[1],flag2) == 0){
      uniq(fd,0,1,0);
    }
    if(strcmp(argv[1],flag3) == 0){
      uniq(fd,0,0,1);


    }

  }

  if(argc == 4){
    if(((strcmp(argv[1],flag1)== 0) && (strcmp(argv[2],flag2) == 0)) ||(((strcmp(argv[1],flag2)== 0 ) && (strcmp(argv[2],flag1)) == 0))){
       uniq(fd,1,1,0);
    }

  }
  close(fd);
}
  exit();
}








