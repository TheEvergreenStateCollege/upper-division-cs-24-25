/**
Conway's Game of LIfe 
serial version
prints a sequence of arrays, one for each time step
using an nxn board of ints with 0, 1
 */
 
 
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// globals
int size = 0;  // for an nxn board
int userGen;
char **board = NULL; // as a 2D array
char **tmp = NULL; // copy of the board for updating


void init_board() {
  int r, c;
  int i;
  char *board_arry = (char *)calloc(size * size, sizeof(char));  //the actual data
  char *tmp_arry = (char *)calloc(size * size, sizeof(char));    //the actual data
  board = (char **)malloc(size * sizeof(char *));
  tmp = (char **)malloc(size * sizeof(char *));

  // initialize the row indices
  #pragma omp parallel for //fill the array with 0's quicker
  for (r=0; r< size; r++) {
    board[r] = board_arry + r * size;  // &board_arry[r * size]
    tmp[r] = tmp_arry + r * size;
  }

  /*
  for (i=0; i<size*size; i++) {
    board_arry[i] = 0;
    tmp_arry[i] = 0;
  }
  */
  
  //kill all cells'
  for (r = 0; r < size; r++) {
      for (c = 0; c < size; c++) {
          board[r][c] = 0;
          tmp[r][c] = 0;
      }
  }
  
  if (size > 2) {
    board[2][1] = 1;
    board[2][2] = 1;
    board[2][3] = 1;
  }
  
}

#pragma omp parallel for //creating threads to update squares per rules 
void update_square(int row, int col) {
  int r,c;
  int sum = 0;
  int alive = board[row][col];
  
   // Count alive neighbors
    for (r = row - 1; r <= row + 1; r++) {
        for (c = col - 1; c <= col + 1; c++) {
            if (r >= 0 && r < size && c >= 0 && c < size) {  
                if (!(r == row && c == col)) {  
                    alive += board[r][c]; 
                }
            }
        }
    }

    // Apply rules 
    if (alive == 1) {  
        if (alive < 2 || alive > 3) {
            tmp[row][col] = 0;  
        } else {
            tmp[row][col] = 1;  
        }
    } else { 
        if (alive == 3) {
            tmp[row][col] = 1;  
        } else {
            tmp[row][col] = 0;  
        }
    }
}

#pragma omp parallel for //loop through array creating temporary copy
void update_board() {
  int r, c;
  for (r=0; r<size; r++) {
      for (c = 0; c < size; c++) {
        update_square(r, c);
  }
}

// Copy tmp board back to the main board
    for (r = 0; r < size; r++) {
        for (c = 0; c < size; c++) {
            board[r][c] = tmp[r][c];
        }
    }
}

void print_board() {
  int r, c;
  for (r=0; r<size; r++) {
    for (c=0; c<size; c++) {
      printf("%d  ", board[r][c]);
    }
    printf("\n");
  }
  return;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    printf("usage: %s boardsize\n", argv[0]);
    exit(EXIT_FAILURE);
  }
  
  //convert argument to int
  char *endptr;
  size = strtol(argv[1], &endptr, 10);
  
  //Error checking for positive int
  if (*endptr != '\0' || size <= 0) {
      printf("Error board not a positive integer. \n");
      exit(EXIT_FAILURE);
  }
  
  //intialize board size
  init_board();
  
  //print intial board
  printf("Initial Board:\n");
  print_board();
  
  
  //Run generations 
  printf("How many generations would you like to run: ");
  scanf("%d", &userGen);
  int steps = userGen;
  for (int i = 0; i < steps; i++) {
      update_board();
      print_board();
  }
  
 
  
  return 0;
}
