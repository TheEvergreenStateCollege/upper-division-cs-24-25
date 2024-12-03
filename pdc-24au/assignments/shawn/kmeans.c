#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <ctype.h>
#include <math.h>
#include <omp.h>
// for compiling on lab mac
//#include "/Users/pngh5239/homebrew/opt/libomp/include/omp.h"

/**
 * k means clustering 
 * parallel version

 * given a set of points [2D] 
 * produce a labeled list of points 
 * where the label is the index of its cluster

 * array of points: x, y, cluster
 * array of clusters: centroid for each cluster
 
 * made by Shawn with the assistance of Austin and Andersen
**/

int groups = 4; // number of clusters, max 26
int size = 10; // number of points
int rarity = 5; // ratio of blanks spaces to points
int aligning = 1; // track centroid convergence

typedef struct point {
  double x, y;
  int cluster;
} point;

typedef struct cluster {
  point *centroid;
  double xsum, ysum;
  int count;
  char mark;
} cluster;

double distance(point *p1, point *p2) {
  return pow(p2->x - p1->x, 2) + pow(p2->y - p1->y, 2) * 1.0;
}

void init_points(point **points) {
  for (int i=0; i < size; i++) {
    point *ptr = (point*)malloc(sizeof(point));
    // set points to random coordinates
    ptr->x = rand() % (size * rarity);
    ptr->y = rand() % (size * rarity);
    ptr->cluster = 0;
    points[i] = ptr;
  }
}

void init_clusters(point **points, cluster **clusters) {
  // make an array of the alphabet to label groupings with
  char marks[26];
  char m = 'a';
  for (int i=0; i < 26; i++) {
    marks[i] = m;
    m++;
  }
  // initialize clusters
  for (int i=0; i < groups; i++) { 
    cluster *cls = (cluster*)malloc(sizeof(cluster));
    cls->mark = marks[i];
    cls->centroid = (point*)malloc(sizeof(point));
    cls->centroid->x = 0;
    cls->centroid->y = 0;
    cls->centroid->cluster = i;
    clusters[i] = cls;
  }
  // use k-means++ algorithm
  int p = rand() % size;
  // align first centroid to a random point
  clusters[0]->centroid->x = points[p]->x;
  clusters[0]->centroid->y = points[p]->y;
  for (int i=1; i < groups; i++) {
    int maxi = 0;
    double farthest = 0;
    #pragma omp parallel for shared(i, maxi, farthest)
    for (int j=0; j < size; j++) {
      double d = DBL_MAX;
      // measure distance to every already aligned centroid
      for (int h=0; h < i; h++) {
        double tmpd = distance(points[j], clusters[h]->centroid);
        if (tmpd < d) {
          d = tmpd;
        }
      }
      // align centroid to the point farthest from other centroids
      if (d > farthest) {
        #pragma omp atomic write
        maxi = j;
        #pragma omp atomic write
        farthest = d;
      }
    }
    clusters[i]->centroid->x = points[maxi]->x;
    clusters[i]->centroid->y = points[maxi]->y;
  }
  /* uncomment to print cluster starting coordinates
  for (int i=0; i < groups; i++) {
    printf("Cluster %c: %d,%d\n", toupper(clusters[i]->mark), (int)clusters[i]->centroid->x, (int)clusters[i]->centroid->y);
  }
  */
}

void assign_and_sum(point **points, cluster **clusters) {
  // save current centroid positions for comparison later
  point **previous = (point**)malloc(groups * sizeof(point*));
  for (int c=0; c < groups; c++) { 
    previous[c] = (point*)malloc(sizeof(point));
    previous[c]->x = clusters[c]->centroid->x;
    previous[c]->y = clusters[c]->centroid->y;
    // set cluster fields to zero for new iteration
    clusters[c]->count = 0;
    clusters[c]->xsum = 0;
    clusters[c]->ysum = 0;
  }
  int i, j;
  // create two dimensional array for reduction later
  point ***sums = (point***)malloc(groups * sizeof(point**));
  for (i=0; i < groups; i++) {
    sums[i] = (point**)malloc(size * sizeof(point*));
    for (j=0; j < size; j++) {
      sums[i][j] = NULL;
    }
  }
  // loop over each point
  #pragma omp parallel for private(i, j) shared(sums)
  for (i=0; i < size; i++) { 
    // set dist to current distance to centroid
    double dist = distance(clusters[points[i]->cluster]->centroid, points[i]);
    // loop over each cluster
    for (j=0; j < groups; j++) {
      double cdist = distance(clusters[j]->centroid, points[i]);
      // if this cluster is closer, assign this point to it
      if (cdist < dist) {
        dist = cdist;
        points[i]->cluster = j;
      }
    }
    // save pointer to sum later
    sums[points[i]->cluster][i] = (point*)points[i];
  }
  // sum the cluster fields
  for(i=0; i < groups; i++) {
    double xsum = 0;
    double ysum = 0;
    int count = 0;
    // reduce pointers in the sums array for this cluster
    #pragma omp parallel for private(j) shared(i) reduction(+:xsum, ysum, count)
    for (j=0; j < size; j++) {
      // skip null pointers
      if (sums[i][j] == NULL) {
        continue;
      }
      xsum += sums[i][j]->x;
      ysum += sums[i][j]->y;
      count += 1;
    }
    // save totals in cluster
    clusters[i]->xsum = xsum;
    clusters[i]->ysum = ysum;
    clusters[i]->count = count;
    free(sums[i]);
  }
  free(sums);
  // align the centroids to the mean of each cluster
  aligning = 0;
  for (int i=0; i < groups; i++) { 
    // avoid divide by zero errors
    int count = 1;
    if (clusters[i]->count > 0) {
      count = clusters[i]->count;
    }
    // set position to the mean of assigned points
    clusters[i]->centroid->x = clusters[i]->xsum / count;
    clusters[i]->centroid->y = clusters[i]->ysum / count;
    // compare new alignment to previous location
    aligning += distance(previous[i], clusters[i]->centroid);
    free(previous[i]);
  }
  free(previous);
}

void print_points(point **points, cluster **clusters) {
  char **locs = (char**)malloc(size * rarity * sizeof(char*));
  for (int i=0; i < size * rarity; i++) {
    locs[i] = (char*)malloc(size * rarity * sizeof(char));
    for (int j=0; j < size * rarity; j++) {
      locs[i][j] = ' ';
    }
  }
  for (int i=0; i < size; i++) {
    int x = (int)points[i]->x;
    int y = (int)points[i]->y;
    // label points with their cluster's letter
    locs[y][x] = clusters[points[i]->cluster]->mark;
  }
  for (int i=0; i < groups; i++) {
    int x = (int)clusters[i]->centroid->x;
    int y = (int)clusters[i]->centroid->y;
    // if the location already contains a point label with cluster index number
    if (locs[y][x] != ' ') {
      locs[y][x] = i + '0';
    } else {
      // label centroids with uppercase cluster letter
      locs[y][x] = toupper(clusters[i]->mark);
    }
  }
  // start printing at end of y axis and beginning of x axis, top down left to right
  for (int i=size * rarity - 1; i >= 0; i--) {
    for (int j=0; j < size * rarity; j++) {
      char symbol = locs[i][j];
      char overlap = ' ';
      // use a '+' to show when a centroid overlaps a point
      if (isdigit(symbol)) {
        int c = symbol - '0';
        symbol = toupper(clusters[c]->mark);
        overlap = '+';
      }
      printf("%c%c", symbol, overlap);
    }
    printf("\n");
  }
  for (int i=0; i < size * rarity; i++) {
    free(locs[i]);
  }
  free(locs);
}

int main(int argc, char **argv) {
  // set groups, size, and rarity from commandline arguments if provided
  if (argc > 2) {
    groups = atoi(argv[1]);
    if (groups < 1 || groups > 26) {
      printf("Number of clusters must be between 1 and 26");
      return 1;
    }
    size = atoi(argv[2]);
    if (size < groups) {
      printf("Number of points must be greater than the number of clusters");
      return 1;
    }
    if (argc > 3) {
      rarity = atoi(argv[3]);
      if (rarity < 1) {
        printf("Rarity must be a number greater than zero.");
        return 1;
      }
    }
  } else if (argc > 1) {
    printf("Usage: %s clusters points [rarity]\n", argv[0]);
    printf("clusters: number of groupings, number between 1-26\n");
    printf("points: number of randomly positioned points to cluster\n");
    printf("rarity: number of empty spaces generated for each point (default 5)\n");
    return 1;
  }

  // set initial values
  srand(time(NULL)); // seed random numbers
  point **point_array;
  cluster **cluster_array;
  point_array = (point**)malloc(size * sizeof(point*));
  cluster_array = (cluster**)malloc(groups * sizeof(cluster*));
  init_points(point_array);
  init_clusters(point_array, cluster_array);
  /* uncomment to print initial alignment
  print_points(point_array, cluster_array);
  printf("---\n");
  */

  // roll out the pie crust
  while (aligning) {
    assign_and_sum(point_array, cluster_array);
    /* uncomment to print each iteration.
    print_points(point_array, cluster_array);
    printf("---\n");
    */
  }

  // print final alignment
  print_points(point_array, cluster_array);

  return 0;
}
