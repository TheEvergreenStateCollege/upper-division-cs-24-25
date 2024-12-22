#include <math.h>
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


void init_points(point *point_list, int length) {
  int i;
  for (i=0; i<length; i++) {
    point_list[i].x = rand();
    point_list[i].y = rand();
    point_list[i].label = 0;
  }
}

void init_cluster(cluster *cluster_list) {
  int i;
  for (i=0; i<K; i++) {
    cluster_list[i].sum.x = rand();
    cluster_list[i].sum.y = rand();
  }
}

double distance(point a, point b) {
  int dx = b.x - a.x;
  int dy = b.y - a.y;
  return sqrt(dx*dx + dy*dy);
}

void assign_and_sum(point *array, cluster *cluster_array) {
  int i, j;
  
  double dist;
  int label;

  // assignment step: label each point to nearest centroid
  // for each point
  for (i=0; i<SIZE; i++) { 
    // for each cluster
    point a = array[i];

    dist = distance(a, cluster_array[a.label].sum);
    printf("point a: %d, dist: %f\n", i, dist);

    for (j=0; j<K; j++) {
    
      point b = cluster_array[j].sum;
      float error = distance(a, b);
      printf("point b: %d, error: %f\n", j, error);

      if (error < dist) {
        a.label = j;
        dist = error;
      }
    }
    
  }
  
  // update step: adjust each centroid to local mean
  int count;
  point accumulator;
  for (j=0; j<K; j++) {
    // for each point
    count = 0;
    accumulator.x = 0;
    accumulator.y = 0;
    for (i=0; i<SIZE; i++) {
      point p = array[i];
      if (p.label == j) {
      	accumulator.x += p.x;
      	accumulator.y += p.y;
      	count += 1;
      }
    }
    if (count == 0) {
      printf("huh\n");
    }
    else {
      printf("ok\n");
    }
    cluster_array[j].sum.x = accumulator.x / count;
    cluster_array[j].sum.y = accumulator.y / count;
  }
}

void print_points(point pt) {
  printf("%f, %f\n", pt.x, pt.y);
}

int main() {
  // SIZE and K are global
  printf("test main\n");
  
  point *points_list;
  cluster *cluster_array;

  printf("test 1\n");

  points_list = (point *)malloc(SIZE * sizeof(point));
  cluster_array = (cluster *)malloc(K * sizeof(cluster));

  printf("test 2\n");

  print_points(cluster_array[0].sum);

  printf("test 3\n");

  init_points(points_list, SIZE);
  init_cluster(cluster_array);

  printf("test 4\n");

  for (int i = 0; i < 10; i++) {
    assign_and_sum(points_list, cluster_array);
    print_points(cluster_array[0].sum);
  }
  
  return 0;
}