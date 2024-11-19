#include <stdio.h>
#include <stdlib.h>


/**
 * k means clustering 
 * serial version

 * given a set of points [2D] 
 * produce a labeled list of points 
 * where the label is a pointer to its cluster

 * array of points: x,y, label
 * array of clusters: centroid for each cluster

 */

int K = 4; //number of clusters

int SIZE = 10;

typedef struct point {
  double x, y;
  int label;
  
} point;

typedef struct cluster {
  point sum;
  int count;
  int name;
} cluster;


void init_points(point *point_list[], int length) {
  int i;
  for (i=0; i<length; i++) {
    point_list[i]-> x = rand();
    point_list[i]-> y = rand();
    point_list[i]-> label = 0;
  }
}


void assign_and_sum(point *array[], int begin, int end, cluster *cluster_array[], int kclusters) {
  int i;

  // for each point
  for (i=begin; i<end; i++) { 
    // for each cluster
    
    
  }
}


int main() {
  // SIZE and K are global
  
  point *points_list[];
  cluster *cluster_array[];

  points_list = (point *)malloc(SIZE * sizeof(point));
  cluster_array = (K * sizeof(cluster));

  
  return 0;
}
