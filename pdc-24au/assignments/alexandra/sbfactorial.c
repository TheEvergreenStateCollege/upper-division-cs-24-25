//#include "/Users/pngh5239/homebrew/opt/libomp/include/omp.h"
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {

    // Get the starting number
    int num = 20; // default
    if (argc > 1) {
        num = atoi(argv[1]);
        if (num > 20) { // !21 is too big for ull int
            printf("Factorial too large, result not accurate.\n");
        }
    }
    
    // Create an array from input number
    int nums[num];
    for(int i = 0; i <= num; i++) {
        nums[i] = i+1;
    }
    
    // Use reduction to multiply factorial
    unsigned long long product = 1; // big int
    int i; // loop index
    #pragma omp parallel for private(i) reduction(*:product)
    for(i = 0; i < num; i++) {
        product *= nums[i];
    }

    // Print the result
    printf("%llu\n", product);

    return 0;
}
