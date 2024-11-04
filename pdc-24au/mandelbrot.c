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
#include <time.h>


int size = 1000;
int **image;
int *img_data;

void create_image() {
  img_data = (int *) malloc(size * size * sizeof(int));
  image = (int **) malloc(size * sizeof(int *));

  for(int r = 0; r < size; r++) {
    image[r] = img_data + r * size;
  }
}

/// row = y coord, i.e. imaginary
/// col = x coord, i.e. real
/// <param name="MaxCount">max iterations of loop before giving up</param>
/// <returns> number of iterations</returns>
//
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

void printPixels(int *pixelBoard) {
  int count = 0;
  /*
  for(int i = 0; i < size; i++) {
    for(int j = 0; j < size; j++) {
      if (count % 10 == 0) {
        printf("\n");
      }
      printf("%d", pixelBoard[i][j]);
      count++;
    }
  }*/

  for (int i = 0; i < size; i++) {
    if (count % 10 == 0) {
      printf("\n");
    }
    printf("%-3d ", pixelBoard[i]);
    count++;
  }
}

int main () {
  clock_t begin = clock();
  // alocate image and image_data
  create_image();
  int count = 0;
  // loop through image and compute color
  // call kernel at every point of a nested for loop
  #pragma omp parallel for //collapse (2)
  for (int i = 0; i < size; i++) {
    //int num = omp_get_thread_num();
    //printf("ID: %d", num);
    for (int j = 0; j < size; j++) {
      image[i][j] = kernel(i, j, size);
    }
  }
  printPixels(img_data);
  clock_t end = clock();
  double time_spent = (double)(end - begin)/ (double)(CLOCKS_PER_SEC);
  printf("\n%lf\n", time_spent);
}

