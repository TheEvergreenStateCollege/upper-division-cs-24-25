/**
Conway's Game of LIfe 
serial version
prints a sequence of arrays, one for each time step

using an nxn board of ints with 0, 1
 */


#include <stdio.h>
#include <stdlib.h>

// globals
int size = 0;  // for an nxn board
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
  
  if (size > 2) {
    board[2][1] = 1;
    board[2][2] = 1;
    board[2][3] = 1;
  }
  
  return;
}

void update_square(int row, int col) {
  int r,c;
  int sum = 0;
  int alive = board[row][col];
  return;
}

void update_board() {
  int r, c;
  for (r=0; r<size; r++) {
    for (c=0; c<size; c++) {
    update_square(r, c);
  }
  return;
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
    printf("usage \ngameOfLife size\n");
    exit(-1);
  }
  size = atoi(argv[1]);  // use strtol()
  init_board();
  print_board();

  
  return 0;
}
