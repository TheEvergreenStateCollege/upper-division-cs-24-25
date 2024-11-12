#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generateList(int list[], int length);
void printList(int list[], int start, int stop);
void quicksort(int list[], int start, int stop);
void swap(int list[], int num1, int num2);

int main() {
	int length;
	printf("Will print the array.\n");
	printf("Enter the size of the list: ");
    scanf("%d", &length);
    printf("\n");

    
    int list[length];
	generateList(list, length);

	// Test Prints
	printf("Before sorting: ");
	printList(list, 0, length);
	printf("\n");
	
	quicksort(list, 0, length-1);

	//Test Prints
	printf("\n");
	printf("After sorting: ");
	printList(list, 0, length);
	

	return 0;
}

void generateList(int list[], int length) {
    // Seed the random number generator with the current time
    srand(time(NULL));
    for (int i = 0; i < length; i++) {
        list[i] = rand() % 100; // Generate random numbers between 0 and 99
    }
}

void printList(int list[], int start, int stop) {
	//List with 1 item in it
	if (start == stop) {
		printf("{%d}\n", list[start]);
		return;
	}

	printf("{");
	for (int i = start; i < stop; i++) {
		if (i == stop-1) {
			printf("%d", list[i]);
			break;
		}
		printf("%d, ", list[i]);
	}
	printf("}\n");
}

void swap(int list[], int i1, int i2) {
	int temp = list[i1];
	list[i1] = list[i2];
	list[i2] = temp;
}

void quicksort(int list[], int start, int stop) {
	//Base case
	if (start >= stop) {
		return;
	}
	if (stop - start == 2) {
		if (list[start] <= list[start+1] &&
			list[start+1] <= list[start+2]) {
			return;
		}
	}

	//Random element will be our pivot
	srand(time(NULL));
	int pivotIndex = rand() % (stop - start + 1) + start;
	int pivot = list[pivotIndex];
	int rightPtr;
	int leftPtr = start - 1;

	printf("Pivot: %d\nBefore Partition: ", pivot);
	printList(list, start, stop+1);

	//Move the pivot to the end of the partition
	swap(list, pivotIndex, stop);

	//Loop through list, if list[i] < pivot, increment leftPtr
	//swap list[leftPtr] list[rightPtr]
	for (rightPtr = start; rightPtr < stop; rightPtr++) {
		if (list[rightPtr] < pivot) {
			leftPtr++;
			swap(list, leftPtr, rightPtr);
		}
	}

	//Move pivot to the correct location
	leftPtr++;
	swap(list, leftPtr, rightPtr);

	printf("After Partition: ");
	printList(list, start, stop+1);

	//Sort left side
	#pragma omp parallel 
	{
	quicksort(list, start, leftPtr-1);
	}	
	#pragma omp parallel
	{
	//Sort right side
	quicksort(list, leftPtr+1, stop);
	}
}

















