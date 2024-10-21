/******************************************************************************

hello threads

*******************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// put signature of hello

int thread_count; // number of threads, global variable

void *hello(void *id) {
    long thread_id = (long) id;
    printf("hello from %ld of %d threads \n", thread_id, thread_count);
    return NULL; 
}

int main(int argc, char *argv[]) { // command line stuff argv0 is the name of the program
    long t_id;    // main is tasked with creating and managing threads
    pthread_t *thread_handles; // declaring a pointer type which will be used as an array not malloced yet no memory yet
    
    thread_count = strtol(argv[1], NULL, 10); 
    thread_handles = (pthread_t *)malloc(thread_count * sizeof(pthread_t)); //we have allocated space for pthread structs info about each thread
    //printf("%s \n", argv[1]);
    
    for (t_id=0; t_id<thread_count; t_id++) { //going to say p thread create and create threads
        pthread_create(&thread_handles[t_id], NULL, hello, (void *) t_id); //give it a function to call
    }
    
    
    return 0;
}