#!/usr/bin/env sh

# Debug mode to see all the file downloading and extracting
set -x
wget // need to copy and paste this externall
zcat spark-3.5.5-bin-hadoop3.tgz | tar xvf -
mv spark-3.5.5 /opt/spark-3.5.5-bin-hadoop
# bin/spark-shell --packages graphframes:graphframes:0.8.4-spark3.5-s_2.12
