#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct lineEntry lineEntry;
struct lineEntry {
      int id;
      char bunType[25];
      char pattyType[25];
      char toppings[25];
};

int main(int argc, char *argv[])
{
      if (argc != 3) 
      {
            printf("Usage: %s <filename> <n> where <filename> is the name of the csv to be loaded and <n> is the length of the csv\n", argv[0]);
            return EXIT_FAILURE;
      }

      int csvLength = atoi(argv[2]);
      FILE *filePointer;
      char *currentLine;
      int bufferSize = 100;
      lineEntry *data;
      int headerSkipped = 0;
      int i = 0;
      char tempString[100];
      // int num;

      lineEntry tempData;

      data = (lineEntry *) malloc(csvLength * sizeof(lineEntry));
      if (data == NULL) 
      {
            printf("Cannot allocate data memory\n");
            return EXIT_FAILURE;
      }

      currentLine = (char *) malloc(bufferSize * sizeof(char));
      if (currentLine == NULL) 
      {
            printf("Cannot allocate buffer memory\n");
            return EXIT_FAILURE;
      }

      filePointer = fopen(argv[1], "r");
      if (filePointer == NULL) 
      {
            printf("Cannot open %s\n", argv[1]);
            return EXIT_FAILURE;
      }

      while (fgets(currentLine, bufferSize, filePointer) != NULL) 
      {
            if (!headerSkipped) 
            {
                  headerSkipped = 1;
                  continue;
            }

            if (strlen(currentLine) == 0) 
            {
                  continue;
            }

            // printf("%s\n", currentLine);
            // scanf("%d", &num);
            
            sscanf(currentLine, "%d,%s", &tempData.id, tempString);

            int j = 0;
            int k = 0;
            while (tempString[j] != ',') 
            {
                  tempData.bunType[k] = tempString[j];
                  j++;
                  k++;
            }
            tempData.bunType[k] = '\0';

            j += 1;
            k = 0;
            while (tempString[j] != ',') 
            {
                  tempData.pattyType[k] = tempString[j];
                  j++;
                  k++;
            }
            tempData.pattyType[k] = '\0';

            j += 1;
            k = 0;
            while (tempString[j] != ',' && tempString[j] != '\0') 
            {
                  tempData.toppings[k] = tempString[j];
                  j++;
                  k++;
            }
            tempData.toppings[k] = '\0';

            data[i] = tempData;

            i++;
      }

      free(lineEntry);
      free(currentLine);
      fclose(filePointer);
      return EXIT_SUCCESS;
}
