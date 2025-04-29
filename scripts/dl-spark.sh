#!/usr/bin/env sh

# Debug mode to see all the file downloading and extracting
set -x
URL=https://dlcdn.apache.org/spark/spark-3.5.5
FILE=spark-3.5.5-bin-hadoop3.tgz
BASEDIR=spark-3.5.5-bin-hadoop3

mkdir ~/Downloads
cd ~/Downloads
wget "$URL/$FILE"
gzcat $FILE | tar xf -
rm $FILE
mv $BASEDIR /opt

# Add spark-shell to path (and also spark-submit)
#./scripts/.shrc

/opt/$BASEDIR/bin/spark-shell --packages graphframes:graphframes:0.8.4-spark3.5-s_2.12
