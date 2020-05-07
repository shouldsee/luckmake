// ***
// *** You MUST modify this file, only the ssort function
// ***

#include <stdio.h>
#include <stdbool.h>

#ifdef TEST_COUNTCHAR

// open a file whose name is filename for reading
// if fopen fails, return false. Do NOT fclose
// if fopen succeeds, read every character from the file
//
// if a character (call it onechar) is between
// 0 and size - 1 (inclusive), increase
// counts[onechar] by one
// You should *NOT* assume that size is 256
// reemember to call fclose
// you may assume that counts already initialized to zero
// size is the size of counts
// you may assume that counts has enough memory space
//
// hint: use fgetc
// Please read the document of fgetc carefully, in particular
// when reaching the end of the file
//
bool countChar(char * filename, int * counts, int size)
{
  // int counts[size]={0};
  FILE *fh = fopen(filename,"r");
  if (fh==NULL){
  }else{
    while (true){
      int curr = fgetc(fh);
      // fprintf(stderr, "%d\n", curr);
      if (curr==-1){
        break;
      }else if(curr>=0 && curr <= size-1){
        counts[curr]++;
      }

    }
    // fprintf(stdout, "%c\n", fgetc(fh));
    // fprintf(stdout, "%c\n", fgetc(fh));
    fclose(fh);
  }

  return true;
}
#endif

#ifdef TEST_PRINTCOUNTS
void printCounts(int * counts, int size)
{
  // fprintf(stderr,"%d,%d,%d,%d",(int)'a',(int)'z',(int)'A',(int)'Z');
  // return;
  // print the values in counts in the following format
  // each line has three items:
  // ind, onechar, counts[ind]
  // ind is between 0 and size - 1 (inclusive)
  // onechar is printed if ind is between 'a' and 'z' or
  // 'A' and 'Z'. Otherwise, print space
  // if counts[ind] is zero, do not print
  int i=-1;
  while (true){
    i++;
    if (i==size){
      break;
    }else{
      // char *curr = i;
      int curr =i;
      if (
        (curr >= (int)'A' && curr <= (int)'Z')||
        (curr >= (int)'a' && curr <= (int)'z')){
       ; 
      }else{
        curr = ' ';
      }
      if (counts[i]>0){
        fprintf(stdout, "%d, %c, %d\n", i, curr, counts[i]);
      }
    }


  }
}
#endif
