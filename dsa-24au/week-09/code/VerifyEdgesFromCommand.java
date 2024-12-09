import java.util.*;
import java.io.*;

public class VerifyEdgesFromCommand extends DirectedGraphTestCommand {
   protected String fromLabel = "";
   protected ArrayList<String> toLabels = new ArrayList<String>();

   public VerifyEdgesFromCommand(String fromVertexLabel, ArrayList<String> toVertexLabels) {
      this.fromLabel = fromVertexLabel;
      this.toLabels = new ArrayList<String>(toVertexLabels);
   }

   @Override
   public boolean execute(PrintWriter testFeedback, DirectedGraph graph) {
      // Find fromVertex
      Vertex fromVertex = graph.getVertex(fromLabel);
      if (fromVertex == null) {
         testFeedback.write("FAIL: getVertex(\"" + fromLabel + "\") returned ");
         testFeedback.write("null for a vertex that should exist\n");
         return false;
      }

      // Ask the graph for edges from fromVertex
      ArrayList<Edge> actual = graph.getEdgesFrom(fromVertex);

      boolean pass = true;
      if (actual.size() == toLabels.size()) {
         for (String toLabel : toLabels) {
            // Get the expected to-vertex
            Vertex expectedTo = graph.getVertex(toLabel);

            // If the actual ArrayList of vertices does not have the edge then the
            // test fails
            if (!hasEdge(actual, fromVertex, expectedTo)) {
               pass = false;
               break;
            }
         }
      }
      else {
         pass = false;
      }

      // Print pass or fail message along with actual and expected collections
      testFeedback.write(pass ? "PASS" : "FAIL");
      testFeedback.write(": Get edges from \"" + fromLabel + "\"\n");
      printEdges(testFeedback, actual, ", ", "  Actual:   {", "}\n");
      testFeedback.write("  Expected: {");
      if (toLabels.size() != 0) {
         testFeedback.write(fromLabel + " to " + toLabels.get(0));
         for (int i = 1; i < (int) toLabels.size(); i++) {
            testFeedback.write(", " + fromLabel + " to " + toLabels.get(i));
         }
      }
      testFeedback.write("}\n");

      return pass;
   }
}
