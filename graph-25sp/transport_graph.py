from pyspark.sql.types import *
from graphframes import *
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .config("spark.jars.packages", "graphframes:graphframes:0.6.0") \
    .getOrCreate()

def create_transport_graph():
    node_fields = [
        StructField("id", StringType(), True),
        StructField("latitude", FloatType(), True),
        StructField("longitude", FloatType(), True),
        StructField("population", IntegerType(), True)
    ]

    nodes = spark.read.csv("data/transport-nodes.csv", header=True,

    schema = StructType(node_fields))
    rels = spark.read.csv("data/transport-relationships.csv", header=True)
    reversed_rels = (rels.withColumn("newSrc", rels.dst)
        .withColumn("newDst", rels.src)
        .drop("dst", "src")
        .withColumnRenamed("newSrc", "src")
        .withColumnRenamed("newDst", "dst")
        .select("src", "dst", "relationship", "cost"))
    relationships = rels.union(reversed_rels)
    relationships.show()
    return GraphFrame(nodes, relationships)

create_transport_graph()