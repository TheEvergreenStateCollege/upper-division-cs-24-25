#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

void HelloWorld( void ) {
    long myid = omp_get_thread_num();
    printf( "Hello world! I am thread %ld\n", myid);
}

int fact(int n) {
    int rest;
    long myid = omp_get_thread_num();
    // omp_set_num_threads(2)
    if (n == 0 || n == 1) {
        return n;
    }

#pragma omp parallel
  #pragma omp single 
  rest = fact(n-1);
  // print thread id
  myid = omp_get_thread_num();
  printf(" thread id %ld  %d\n", myid, n);

  //#pragma op taskwait
  return n * rest;
}

int main(void) {
    int res;
    res = fact(22);
    HelloWorld();
    printf(" result %d\n", res);
}