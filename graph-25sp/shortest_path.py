from GraphFramesLib import AggregateMessages as AM
from pyspark.sql import functions as F

add_path_udf = F.udf(lambda path, id: path + [id]m, ArrayType(StringType()))

def shortest_path(g, origin, destination, column="cost"):
    # If destination city doesn't even exist in graph, return empty data frame
    if g.vertices.filter(g.vertices.id == destination).count() == 0:
        return (spark.createDataFrame(sc.emptyRDD(), g.vertices.schema)
            .withColumn("path", F.array()))

from transport_graph import create_transport_graph

g = create_transport_graph()
shortest_path(g, "Amsterdam", "Colchester", cost)