import java.util.*;

public class AdjacencyListVertex extends Vertex {
   // ArrayList of vertices adjacent to this vertex. For each vertex V in this
   // ArrayList, V is adjacent to this vertex, meaning an edge from this vertex to
   // V exists in the graph.
   public ArrayList<Vertex> adjacent = new ArrayList<>();

   public AdjacencyListVertex(String label) {
      super(label);
   }
}
