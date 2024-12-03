import java.util.*;

public class AdjacencyListGraph extends DirectedGraph {
   protected ArrayList<AdjacencyListVertex> vertices = new ArrayList<>();

   // Creates and adds a new vertex to the graph, provided a vertex with the
   // same label doesn't already exist in the graph. Returns the new vertex on
   // success, null on failure.
   @Override
   public Vertex addVertex(String newVertexLabel) {
      // TODO: Type your code here (remove placeholder line below)
      return null;
   }

   // Adds a directed edge from the first to the second vertex. If the edge
   // already exists in the graph, no change is made and false is returned.
   // Otherwise the new edge is added and true is returned.
   @Override
   public boolean addDirectedEdge(Vertex fromVertex, Vertex toVertex) {
      // TODO: Type your code here (remove placeholder line below)
      return false;
   }

   // Returns an ArrayList of edges with the specified fromVertex.
   @Override
   public ArrayList<Edge> getEdgesFrom(Vertex fromVertex) {
      // TODO: Type your code here (remove placeholder line below)
      return new ArrayList<Edge>();
   }

   // Returns an ArrayList of edges with the specified toVertex.
   @Override
   public ArrayList<Edge> getEdgesTo(Vertex toVertex) {
      // TODO: Type your code here (remove placeholder line below)
      return new ArrayList<Edge>();
   }

   // Returns a vertex with a matching label, or null if no such vertex
   // exists
   @Override
   public Vertex getVertex(String vertexLabel) {
      // TODO: Type your code here (remove placeholder line below)
      return null;
   }

   // Returns true if this graph has an edge from fromVertex to toVertex
   @Override
   public boolean hasEdge(Vertex fromVertex, Vertex toVertex) {
      // TODO: Type your code here (remove placeholder line below)
      return false;
   }
}
