#!/usr/bin/env sh

# Debug mode to see all the file downloading and extracting
set -x
URL=https://dlcdn.apache.org/spark/spark-3.5.5
FILE=spark-3.5.5-bin-hadoop3.tgz

mkdir ~/Downloads; cd ~/Downloads
wget "$URL/$FILE"
zcat $FILE | tar xf -
rm $FILE
mv spark-3.5.5-bin-hadoop3 /opt
