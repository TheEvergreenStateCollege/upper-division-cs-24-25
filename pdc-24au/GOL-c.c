#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main(){
    
	srand(time(NULL));

	int boardWidth = 64;
	int boardHeight = 64;

	int board1[boardWidth][boardHeight];
	int board2[boardWidth][boardHeight];

	int neighbors[boardWidth][boardHeight];

	int dir[8][2] = {{1,0},{1,-1},{0,-1},{-1,-1},{-1,0},{-1,1},{0,1},{1,1}};
	int born[9] = {0,0,0,1,0,0,0,0,0};
	int survive[9] = {0,0,1,1,0,0,0,0,0};

	int loops = 0;
		
	//Setting up board
	for(int i = 0; i < boardWidth; ++i){
		for(int j = 0; j < boardHeight; ++j){
			
			board1[i][j] = rand() % 2;
			board2[i][j] = board1[i][j];
		}
	}
    
	//Looping
	while(loops <= 1000){
			
		//Copying
		for(int i = 0; i < boardWidth; ++i){
			for(int j = 0; j < boardHeight; ++j){

				for(int k = 0; board2[i][j] == 1 && k < 8; ++k){

					++neighbors[i + dir[k][0]][j + dir[k][1]];
				}
			
				board1[i][j] = board2[i][j];
			}
		}
			
		system("clear");
		
		//Interacting
		for(int i = 0; i < boardWidth; ++i){
			for(int j = 0; j < boardHeight; ++j){
				
				if(board1[i][j] == 1){
				
					printf("O");

					for(int k = 0; k < 8; ++k){

						if(neighbors[i][j] == k){
							
							board2[i][j] = survive[k];
							break;
						}
					}
		
					neighbors[i][j] = 0;
					continue;
				}
				
				printf(" ");

				for(int k = 0; k < 8; ++k){

					if(neighbors[i][j] == k){
						
						board2[i][j] = born[k];
						break;
					}
				}
			
				neighbors[i][j] = 0;
			}
			printf("\n");
		}
		
		++loops;
		usleep( 60000 );
	}

    return 0;
}