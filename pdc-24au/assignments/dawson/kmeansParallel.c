#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define K 4        // Number of clusters
#define SIZE 10    // Number of points
#define MAX_ITER 10

typedef struct point {
    double x, y;
    int label; // Index of the cluster
} point;

typedef struct cluster {
    double x, y; // Centroid
    int count;   // Number of points in the cluster
} cluster;

// Function to initialize points with random values
void init_points(point points[], int length) {
    for (int i = 0; i < length; i++) {
        points[i].x = rand() % 100; // Random x-coordinate (0 to 99)
        points[i].y = rand() % 100; // Random y-coordinate (0 to 99)
        points[i].label = -1;       // No cluster assigned initially
    }
}

// Function to initialize cluster centroids with random points
void init_clusters(cluster clusters[], point points[], int kclusters) {
    for (int i = 0; i < kclusters; i++) {
        clusters[i].x = points[i].x; // Use first K points as initial centroids
        clusters[i].y = points[i].y;
        clusters[i].count = 0;
    }
}

// Calculate the Euclidean distance between two points
double euclidean_distance(double x1, double y1, double x2, double y2) {
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

// Assign points to the nearest cluster and sum their coordinates
void assign_and_sum(point points[], int num_points, cluster clusters[], int kclusters) {
    int i, j;

    // Parallel assignment of points to clusters
    #pragma omp parallel for private(j)
    for (i = 0; i < num_points; i++) {
        int thread_id = omp_get_thread_num();
        printf("Thread %d processing point %d\n", thread_id, i);


        double min_distance = __DBL_MAX__;
        int closest_cluster = -1;

        for (j = 0; j < kclusters; j++) {
            double distance = euclidean_distance(points[i].x, points[i].y, clusters[j].x, clusters[j].y);
            if (distance < min_distance) {
                min_distance = distance;
                closest_cluster = j;
            }
        }

        // Assign point to the closest cluster
        points[i].label = closest_cluster;
    }

    // Initialize temporary arrays for cluster sums
    double temp_sum_x[K] = {0};
    double temp_sum_y[K] = {0};
    int temp_count[K] = {0};

    // Parallel accumulation of cluster sums
    #pragma omp parallel for reduction(+:temp_sum_x[:K], temp_sum_y[:K], temp_count[:K])
    for (i = 0; i < num_points; i++) {
        int cluster_id = points[i].label;
        temp_sum_x[cluster_id] += points[i].x;
        temp_sum_y[cluster_id] += points[i].y;
        temp_count[cluster_id]++;
    }

    // Update cluster data
    for (j = 0; j < kclusters; j++) {
        clusters[j].x = temp_sum_x[j];
        clusters[j].y = temp_sum_y[j];
        clusters[j].count = temp_count[j];
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

int main(int argc, char *argv[]) {
    point points[SIZE];
    cluster clusters[K];

    // Allow user to specify the number of threads
    int num_threads = 8; // Default number of threads
    if (argc > 1) {
        num_threads = atoi(argv[1]);
    }

    // Set the number of threads
    omp_set_num_threads(num_threads);

    // Output the number of threads
    printf("Running with %d threads\n", omp_get_max_threads());

    // Initialize points and clusters
    init_points(points, SIZE);
    init_clusters(clusters, points, K);

    // K-means clustering iterations
    for (int iter = 0; iter < MAX_ITER; iter++) {
        printf("Iteration %d\n", iter + 1);
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