#!/bin/sh

# Build the class files first, GameOfLife.class
java *.java
# Convert class bytecode to native binary with GraalVM Ahead-Of-Time compilation
native-image -cp . GameOfLife -o gameoflife-default
# Time the executable

