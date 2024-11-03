#include <stdio.h>
#include <stdlib.h>



/**
 * serial version of quicksort
 * recursive.
 * at the end of each partition are the elements from start through i-1 (inclusive) 
 * less than or equal to the pivot value?
 */

void print_array(int arr[], int start, int stop) {
  int i;

  for (i=start; i<= stop; i++) {
    printf("%d,  ", arr[i]);
  }
  printf("\n");
}


/*
return the position of the pivot
 */
int partition(int start, int stop, int *arr) {
  int pivot = arr[stop];
  int i = start;
  int tmp = 0;
  
  for (int j=start; j<stop; j++) {
    if (arr[j] <= pivot) {
      tmp = arr[i];
      arr[i] = arr[j];
      arr[j] = tmp;
      i++;
    }
  }
  tmp = arr[i];
  arr[i] = arr[stop];
  arr[stop] = tmp;
    
  return i;
}


// start to stop inclusive
void quicksort(int start, int stop, int *arr) {

  int i = start, j = start;

  // base cases for recursion
  if (start >= stop || start < 0) {
    return;  
  }
    
  // Partition array and get the pivot index
    int p = partition(start, stop, arr);

    quicksort(start, p - 1, arr);
    quicksort(p + 1, stop, arr);
  
  return;
}

int main() {
  int SIZE = 8;
  int arr[] = {3,2,9, 8,7,1, 0,5};


  // todo: open file for reading data

  // generate an array of int of size 8 for testing
  
  // print the array

  //call quicksort
  quicksort(0, SIZE - 1, arr);
  // print the sorted array
  print_array(arr, 0, SIZE - 1);
  return 0;
}
