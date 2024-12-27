#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

/**
 * Serial version of quicksort (recursive).
 * At the end of each partition, the elements from start through i-1 (inclusive) 
 * are less than or equal to the pivot value.
 */

void print_array(int arr[], int start, int stop) {
  int i;

  for (i = start; i <= stop; i++) {
    printf("%d,  ", arr[i]);
  }
  printf("\n");
}

/*
 * Return the position of the pivot after partitioning.
 */
int partition(int start, int stop, int *arr) {
  int pivot = arr[stop];
  int i = start;
  int tmp = 0;
  
  for (int j = start; j < stop; j++) {
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
  // base cases for recursion
  if (start >= stop || start < 0) {
    return;  
  }
    
  // Partition array and get the pivot index
  int p = partition(start, stop, arr);

  // Recursively sort the left and right partitions
  #pragma omp parallel sections
  {
    #pragma omp section
    {
        quicksort(start, p - 1, arr);
    }
    #pragma omp section
    {
        quicksort(p + 1, stop, arr);
    }
  }
  
}

int main() {
  // Randomize version of the array, delete the comment if you want to use it
  int SIZE = 20;
  int arr[SIZE];

  srand(time(NULL));

  for (int i = 0; i < SIZE; i++) {
    arr[i] = rand() % 100; // Generate numbers between 0 and 99
  }

  // int arr[] = {3, 2, 9, 8, 7, 1, 0, 5, 4, 6};
  // int SIZE = sizeof(arr) / sizeof(arr[0]);

  // Print the original array
  printf("Original array:\n");
  print_array(arr, 0, SIZE - 1);

  // Call quicksort
  #pragma omp parallel
  {
    #pragma omp single
    {
        quicksort(0, SIZE - 1, arr);
    }
  }

  // Print the sorted array
  printf("Sorted array:\n");
  print_array(arr, 0, SIZE - 1);

  return 0;
}
