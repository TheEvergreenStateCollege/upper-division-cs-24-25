#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define K 4       // Number of clusters
#define SIZE 10   // Number of points
#define MAX_ITER 100

typedef struct point {
    double x, y;
    int label; // Index of the cluster
} point;

typedef struct cluster {
    double x, y; // Centroid
    int count;   // Number of points in the cluster
} cluster;

// Initialize points with random values
void init_points(point points[], int length) {
    for (int i = 0; i < length; i++) {
        points[i].x = rand() % 100; // Random x-coordinate (0 to 99)
        points[i].y = rand() % 100; // Random y-coordinate (0 to 99)
        points[i].label = -1;       // No cluster assigned initially
    }
}

// Initialize cluster centroids with random points
void init_clusters(cluster clusters[], point points[], int kclusters) {
    for (int i = 0; i < kclusters; i++) {
        clusters[i].x = points[i].x; // Use first K points as initial centroids
        clusters[i].y = points[i].y;
        clusters[i].count = 0;
    }
}

// Calculate the distance between two points
double euclidean_distance(double x1, double y1, double x2, double y2) {
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

// Assign points to the nearest cluster and sum their coordinates
void assign_and_sum(point points[], int num_points, cluster clusters[], int kclusters) {
    for (int i = 0; i < kclusters; i++) {
        clusters[i].count = 0; // Reset count and sums
        clusters[i].x = 0;
        clusters[i].y = 0;
    }

    for (int i = 0; i < num_points; i++) {
        double min_distance = __DBL_MAX__;
        int closest_cluster = -1;

        for (int j = 0; j < kclusters; j++) {
            double distance = euclidean_distance(points[i].x, points[i].y, clusters[j].x, clusters[j].y);
            if (distance < min_distance) {
                min_distance = distance;
                closest_cluster = j;
            }
        }

        // Assign the point to the closest cluster
        points[i].label = closest_cluster;

        // Add the point's coordinates to the cluster's sum
        clusters[closest_cluster].x += points[i].x;
        clusters[closest_cluster].y += points[i].y;
        clusters[closest_cluster].count++;
    }
}

// Update cluster centroids
void update_clusters(cluster clusters[], int kclusters) {
    for (int i = 0; i < kclusters; i++) {
        if (clusters[i].count > 0) {
            clusters[i].x /= clusters[i].count; // Calculate the mean x-coordinate
            clusters[i].y /= clusters[i].count; // Calculate the mean y-coordinate
        }
    }
}

int main() {
    point points[SIZE];
    cluster clusters[K];

    // Initialize points and clusters
    init_points(points, SIZE);
    init_clusters(clusters, points, K);

    // K-means clustering iterations
    for (int iter = 0; iter < MAX_ITER; iter++) {
        // printf("Iteration %d\n", iter + 1);
        assign_and_sum(points, SIZE, clusters, K);
        update_clusters(clusters, K);
    }

    // Output results
    for (int i = 0; i < SIZE; i++) {
        printf("Point (%.2f, %.2f) -> Cluster %d\n", points[i].x, points[i].y, points[i].label);
    }

    for (int i = 0; i < K; i++) {
        printf("Cluster %d: Centroid (%.2f, %.2f), Count %d\n", i, clusters[i].x, clusters[i].y, clusters[i].count);
    }

    return 0;
}
