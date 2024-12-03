//Mine isn't running consistently, I think it might be my VSCode, I can get it compiled but haven't seen the returning ASCII art


#include <stdio.h>
#include <stdlib.h>
#include <omp.h>


#define MAX_ITER 1000

void mandelbrot(int width, int height, char **output) {

    //Defining the range of the Mandelbrot set

    double min_real = -2.0;
    double max_real = 1.0;
    double min_imag = -1.0;
    double max_imag = 1.0;

    //Step sizes for the real and imaginary parts

    double real_step = (max_real - min_real) / width;
    double imag_step = (max_imag - min_imag) / height;


    #pragma omp parallel for collapse(2) schedule(dynamic)
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            double real = min_real + x * real_step;
            double imag = min_imag + y * imag_step;
            double z_real = 0.0;
            double z_imag = 0.0;
            int n = 0;

            //check how many iterations it takes for the point to escape the set

            while (z_real * z_real + z_imag * z_imag <= 4.0 && n < MAX_ITER) {
                double z_real_temp = z_real * z_real - z_imag * z_imag + real;
                z_imag = 2.0 * z_real * z_imag + imag;
                z_real = z_real_temp;
                n++;
            }

            //store the ASCII character in the 2D array

            if (n == MAX_ITER) {
                output[y][x] = '#'; //the point is in the set
            } else {
                output[y][x] = ' '; //the point escaped
            }
        }
    }
}


void print_mandelbrot(int width, int height, char **output) {
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            printf("%c", output[y][x]);
        }
        printf("\n");
    }
}


int main(int argc, char *argv[]) {

    //Ensure width and height from user

    if (argc < 3) {
        printf("Usage: %s <width> <height>\n", argv[0]);
        return 1;
    }

    //Get width and height from command-line

    int width = atoi(argv[1]);
    int height = atoi(argv[2]);

    //check height and width are valid

    if (width <= 0 || height <= 0) {
        printf("Invalid dimensions. Please try again.");
        return 1;
    }

    //Dynamically allocate memory for the 2D array
    
    char **output = (char **)malloc(height * sizeof(char *));
    for (int i = 0; i < height; i++) {
        output[i] = (char *)malloc(width * sizeof(char));
    }

    //Generate the Mandelbrot set in parallel
    mandelbrot(width, height, output);

    //free allocated memory
    for (int i = 0; i < height; i++) {
        free(output[i]);
    }
    free(output);

    return 0;
}