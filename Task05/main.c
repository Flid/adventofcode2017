#include <stdio.h> 
#include <stdlib.h> 
const char* filename = "data.txt";
#define BUF_SIZE 2048

void perform_jumps(int *cells, int len, unsigned int *result) {
    *result = 0;
    unsigned int pos = 0;
    
    while(1) {
      (*result)++;
      int current_value = cells[pos];
      cells[pos] = current_value + 1;
      pos += current_value;
      
      if(pos < 0 || pos >= len) {
        return;
      }
    }
}

int main() {
     FILE *fp = fopen(filename, "r");
     if(fp == NULL) {
        printf("Failed to open file %s\n", filename); 
        return 1;
     }
     
     int *cells = (int *)calloc(BUF_SIZE, sizeof(int));
     int count = 0;
     char *line = NULL;
     size_t len = 0;
     ssize_t read;
     
     // Read all lines, convert to int, write to *cells.
     while((read = getline(&line, &len, fp)) != -1) {
         cells[count] = atoi(line);
         printf("%i\n", cells[count]);
         count++;
     }
     
     // Clean up
     free(line);
     fclose(fp);
     free(cells);
     
     unsigned int jumps_count;
     perform_jumps(cells, count, &jumps_count);
     
     printf("Total jumps count: %i\n", jumps_count);
     return 0;
 }
