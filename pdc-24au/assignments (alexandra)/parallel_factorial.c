#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
int main(void) {
    unsigned long long result = 1;
    int input = 0;
    printf("Enter number to compute the factorial of: ");
    scanf("%d", &input);
    if(input < 0) {
        printf("Number must be non-negative. Please run the program again with a larger number.\n");
        exit(EXIT_FAILURE);
    }
    if((input == 0) || (input == 1)) {
        printf("%d! = 1\n(%d factorial is 1)\n", input, input);
        return 0;
    }
    if(input >= 20) {
        printf("Calculating the factorial of a number this large will result in a number too large to store. Run this program with a smaller number (i.e. 19).\n");
        exit(EXIT_FAILURE);
    }
    #pragma omp parallel reduction(*: result)
    if((omp_get_num_threads() >= input) && (omp_get_thread_num() >= input)) {
    }
    else {
        if((input % omp_get_num_threads()) != 0) {
            for(int i = (omp_get_thread_num() + 1); i < ((int)(input / omp_get_num_threads()) * (omp_get_thread_num() + 1)); i++) {
                result *= i;
            }
            if(omp_get_thread_num() < (input % omp_get_num_threads())) {
                result *= (int)(input / omp_get_num_threads()) * omp_get_num_threads() + omp_get_thread_num() + 1;
            }
        }
        else {
            for(int i = (omp_get_thread_num() + 1); i < ((int)(input / omp_get_num_threads()) * (omp_get_thread_num() + 1)); i++) {
                result *= i;
            }
        }
    }
    printf("%d! = %lld\n(%d factorial is %lld)\n", input, result, input, result);
    return 0;
}
