#include "/Users/pngh5239/homebrew/opt/libomp/include/omp.h"
//#include <omp.h>
#include <stdio.h>

int max_i = 255;
int size = 100;

int Mandel(double re, double im) {
    double zre = 0;
    double zim = 0;
    double re2 = 0;
    double im2 = 0;
    int limit = 0;
    int i;
    for (i = 0; re2 + im2 <= 4 && i < max_i; i++) {
        zim = 2 * zre * zim + im;
        zre = re2 - im2 + re;
        re2 = zre * zre;
        im2 = zim * zim;
        limit++;
    }
    return limit;
}

int main() {
    int i, j;
    #pragma parallel for private(i, j) collapse(2)
    for (i = 0; i < size; i++) {
        for (j = 0; j < size; j++) {
            if (Mandel(i, j) == max_i) {
                printf("@");
            }
        }
        printf("\n");
    }
    return 0;
}
