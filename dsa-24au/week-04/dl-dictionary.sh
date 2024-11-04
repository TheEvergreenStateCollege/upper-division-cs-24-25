#!/usr/bin/env bash

FILENAME="data/pg29765.txt"
if [ ! -e "${FILENAME}" ]; then
    wget https://www.gutenberg.org/cache/epub/29765/pg29765.txt
fi