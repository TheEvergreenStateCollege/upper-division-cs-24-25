import java.io.*;

public class Edge {
   public Vertex fromVertex;
   public Vertex toVertex;

   public Edge(Vertex from, Vertex to) {
      fromVertex = from;
      toVertex = to;
   }

   @Override
   public boolean equals(Object o) {
      if (o == this) {
         return true;
      }

      if (!(o instanceof Edge)) {
         return false;
      }

      Edge other = (Edge) o;
      return fromVertex == other.fromVertex && toVertex == other.toVertex;
   }

   // Prints this edge in the form "A to B", where "A" is fromVertex's label
   // and "B" is toVertex's label.
   public void print(PrintWriter output) {
      fromVertex.print(output);
      output.write(" to ");
      toVertex.print(output);
   }
}
