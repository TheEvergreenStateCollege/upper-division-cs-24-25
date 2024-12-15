#include <stdio.h>
#include <stdlib.h>
#include <time.h>  // Include for time-based random seed

// Globals
int size = 0;  // for an (n+2)x(n+2) board with padding
char **board = NULL; // 2D array for the current board
char **tmp = NULL;   // 2D array for the temporary board

// Function to initialize the board with padding and random values
void init_board() {
    int r, c;
    // Allocate memory for the board and tmp arrays with extra space for padding
    char *board_arry = (char *)calloc((size + 2) * (size + 2), sizeof(char));  // the actual data
    char *tmp_arry = (char *)calloc((size + 2) * (size + 2), sizeof(char));    // the actual data
    board = (char **)malloc((size + 2) * sizeof(char *));
    tmp = (char **)malloc((size + 2) * sizeof(char *));
    
    // Initialize the row pointers
    for (r = 0; r < size + 2; r++) {
        board[r] = board_arry + r * (size + 2);
        tmp[r] = tmp_arry + r * (size + 2);
    }

    // Seed the random number generator for random board initialization
    srand(time(NULL));  // Use current time to seed the random number generator

    // Initialize the board with random values (0 or 1)
    for (r = 1; r <= size; r++) {
        for (c = 1; c <= size; c++) {
            board[r][c] = rand() % 2;  // Randomly assign 0 or 1
        }
    }
}

// Function to print the board (without the padding)
void print_board() {
    int r, c;
    for (r = 1; r <= size; r++) {
        for (c = 1; c <= size; c++) {
            printf("%d ", board[r][c]);
        }
        printf("\n");
    }
    printf("\n");
}

// Function to count live neighbors of a given cell (excluding the padding)
int count_live_neighbors(int row, int col) {
    int live_neighbors = 0;
    int r, c;
    for (r = -1; r <= 1; r++) {
        for (c = -1; c <= 1; c++) {
            if (!(r == 0 && c == 0)) {  // Don't count the cell itself
                live_neighbors += board[row + r][col + c];
            }
        }
    }
    return live_neighbors;
}

// Function to update a single square based on its neighbors
void update_square(int row, int col) {
    int live_neighbors = count_live_neighbors(row, col);
    
    if (board[row][col] == 1) {
        // A live cell with fewer than 2 or more than 3 live neighbors dies
        if (live_neighbors < 2 || live_neighbors > 3) {
            tmp[row][col] = 0;
        } else {
            tmp[row][col] = 1;  // Cell survives
        }
    } else {
        // A dead cell with exactly 3 live neighbors becomes a live cell
        if (live_neighbors == 3) {
            tmp[row][col] = 1;
        } else {
            tmp[row][col] = 0;  // Cell remains dead
        }
    }
}

// Function to update the entire board by writing to the temporary copy
void update_board() {
    int r, c;

    // Use OpenMP to parallelize the iteration over the board
    #pragma omp parallel for private(c) shared(board, tmp, size)
    for (r = 1; r <= size; r++) {
        for (c = 1; c <= size; c++) {
            update_square(r, c);
        }
    }

    // Swap the board and tmp arrays
    char **temp_ptr = board;  // Use char** instead of char*
    board = tmp;              // Assign tmp to board
    tmp = temp_ptr;           // Assign old board to tmp
}

// Main function
int main(int argc, char **argv) {
    if (argc != 2) {
        printf("usage: %s size\n", argv[0]);
        exit(-1);
    }
    
    size = atoi(argv[1]);  // Get the board size from the command line argument
    if (size <= 0) {
        printf("Board size must be a positive integer.\n");
        exit(-1);
    }

    // Initialize the board
    init_board();

    // Print the initial board
    printf("Initial board:\n");
    print_board();

    // Simulate generations
    int generations = 5;  // You can change this or take it as an input
    for (int gen = 0; gen < generations; gen++) {
        printf("Generation %d:\n", gen + 1);
        update_board();   // Update the board for the next generation
        print_board();    // Print the board
    }

    // Free the allocated memory
    free(board[0]);
    free(board);
    free(tmp[0]);
    free(tmp);

    return 0;
}
