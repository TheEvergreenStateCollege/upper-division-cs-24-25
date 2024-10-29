#include <stdio.h>
#include <omp.h>       // OpenMP

int main(int argc, char** argv) {

    printf("\nBefore...\n");

    #pragma omp parallel
    {
    int id = omp_get_thread_num();
    int numThreads = omp_get_num_threads();
    printf("Hello from thread %d of %d\n", id, numThreads);
    }

    printf("\n\nAfter...\n\n");

    return 0;
}
