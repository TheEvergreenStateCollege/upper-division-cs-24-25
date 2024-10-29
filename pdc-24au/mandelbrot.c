/**
* compute the Mandelbrot set by
* iterating the function z * z + c to
* see where it diverges

*
*/

#include <math.h>   
#include <stdio.h>
#include <complex.h>
#include <stdlib.h>


int size = 400;
int **image;
int *img_data;

void create_image() {
  img_data = (int *) malloc(size * size * sizeof(int));
  image = (int **) malloc(size * sizeof(int *));
}

int main () {
  // alocate image and image_data
  create_image();
  
  // loop through image and compute color
}

/// row = y coord, i.e. imaginary
/// col = x coord, i.e. real
/// <param name="MaxCount">max iterations of loop before giving up</param>
/// <returns> number of iterations</returns>
int kernel(int row, int col, int MaxCount) {
    int i;
    double complex z = 0;
    double complex c = col + row * I;
    i = 0;
    while (i<MaxCount && cabs(z) < 2.0) {
        z = z * z + c;
        i++;
    }
    printf("%f + %f * i\n", creal(z), cimag(z));
    return i;
}
