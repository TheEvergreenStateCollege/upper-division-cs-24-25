#include <stdio.h>
#include <math.h>

int main() {
    int array [9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int i;
    int sum;

    for (i=sizeof(array); i > 0; i--) {
        sum = array[i] * array[i-1];
    }
    printf("%d\n", sum);
    return 0;
}