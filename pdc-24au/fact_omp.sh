#!/usr/bin/env sh
gcc -o fact_omp ./fact_omp.c -lgomp

# Run with
# ./fact_omp