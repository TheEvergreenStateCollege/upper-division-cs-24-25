#include <omp.h>
#include <stdio.h>

int factorial (int num);

int main () {

	int i = 1;
	#pragma omp parallel private(i)
	{
		#pragma omp single
		{
			for (i = 0; i < 17; i++) {
				#pragma omp task
				printf("%d! = %d\n", i, factorial(i));
			}
		}
	} //barrier

	return 0;
}

int factorial (int num) {
	if (num <= 1) {
		return num;
	}
	return factorial(num - 1) * num;
}
