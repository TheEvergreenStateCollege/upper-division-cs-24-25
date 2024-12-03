import java.util.*;
import java.io.*;

public abstract class DirectedGraphTestCommand {
   // Returns true if the test passes, false if the test fails
   public abstract boolean execute(PrintWriter testFeedback, DirectedGraph graph);

   // Utility function that checks if an ArrayList of edges has a particular edge
   public boolean hasEdge(ArrayList<Edge> edges, Vertex fromVertex, Vertex toVertex) {
      // Iterate through the ArrayList's edges
      for (Edge edge : edges) {
         if (edge.fromVertex == fromVertex && edge.toVertex == toVertex) {
            return true;
         }
      }
      return false;
   }

   public void printEdges(PrintWriter output, ArrayList<Edge> edges, String separator, String prefix, String suffix) {
      // Print the prefix string first
      output.write(prefix);

      // Print edges
      if (edges.size() != 0) {
         edges.get(0).print(output);
         for (int i = 1; i < (int) edges.size(); i++) {
            output.write(separator);
            edges.get(i).print(output);
         }
      }

      // Print suffix string
      output.write(suffix);
   }
}
