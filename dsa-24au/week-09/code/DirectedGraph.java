import java.util.*;

// Abstract base class for a directed, non-weighted graph
public abstract class DirectedGraph {
   // Creates and adds a new vertex to the graph, provided a vertex with the
   // same label doesn't already exist in the graph. Returns the new vertex on
   // success, null on failure.
   public abstract Vertex addVertex(String newVertexLabel);

   // Adds a directed edge from the first to the second vertex. No change is
   // made and false is returned if the edge already exists in the graph.
   // Otherwise the new edge is added and true is returned.
   public abstract boolean addDirectedEdge(Vertex fromVertex, Vertex toVertex);

   // Returns an ArrayList of edges with the specified fromVertex.
   public abstract ArrayList<Edge> getEdgesFrom(Vertex fromVertex);

   // Returns an ArrayList of edges with the specified toVertex
   public abstract ArrayList<Edge> getEdgesTo(Vertex toVertex);

   // Returns a vertex with a matching label, or null if no such vertex
   // exists
   public abstract Vertex getVertex(String vertexLabel);

   // Returns true if this graph has an edge from fromVertex to toVertex
   public abstract boolean hasEdge(Vertex fromVertex, Vertex toVertex);
}
