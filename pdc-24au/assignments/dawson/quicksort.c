#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

// Function to print the array from start to stop index
void print_array(int arr[], int start, int stop) {
    for (int i = start; i <= stop; i++) {
        printf("%d,  ", arr[i]);
    }
    printf("\n");
}

// Function to partition the array and return the position of the pivot
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

// Recursive quicksort function with OpenMP tasks for parallelism
void quicksort(int start, int stop, int *arr) {
    if (start >= stop) {
        return;
    }

    int p = partition(start, stop, arr);
    int threshold = 1; // kept low for now for testing

    // Only create tasks if the size of the subarray is above the threshold
    if ((stop - start) > threshold) {
        #pragma omp task shared(arr)
        {
            printf("Thread %d sorting left part: arr[%d:%d]\n", omp_get_thread_num(), start, p - 1);
            quicksort(start, p - 1, arr);  // Left part
        }

        #pragma omp task shared(arr)
        {
            printf("Thread %d sorting right part: arr[%d:%d]\n", omp_get_thread_num(), p + 1, stop);
            quicksort(p + 1, stop, arr);  // Right part
        }

        #pragma omp taskwait  // Ensure both tasks complete before moving on
    } else {
        // Sort sequentially if below the threshold
        quicksort(start, p - 1, arr);
        quicksort(p + 1, stop, arr);
    }
}

// Wrapper function to start parallel region and call quicksort
void parallel_quicksort(int start, int stop, int *arr) {
    #pragma omp parallel
    {
        #pragma omp single
        quicksort(start, stop, arr);
    }
}

// Function to generate a random list of integers
void generateList(int list[], int length) {
    srand(time(NULL));
    for (int i = 0; i < length; i++) {
        list[i] = rand() % 100;  // Random numbers between 0 and 99
    }
}

int main() {
    int size;
    printf("Enter the size of the list: ");
    scanf("%d", &size);
    printf("\n");

    int arr[size];
    generateList(arr, size);

    printf("Array pre sorted: ");
    print_array(arr, 0, size - 1);
    printf("\n");

    // Call the wrapper function to start parallel quicksort
    parallel_quicksort(0, size - 1, arr);

    printf("Sorted array: ");
    print_array(arr, 0, size - 1);
    return 0;
}
