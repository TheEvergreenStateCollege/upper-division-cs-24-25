#!/usr/bin/env

# Debug mode to see all the file downloading and extracting
set -x
RUN wget https://www.apache.org/dyn/closer.lua/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz
bin/spark-shell --packages graphframes:graphframes:0.8.4-spark3.5-s_2.12
