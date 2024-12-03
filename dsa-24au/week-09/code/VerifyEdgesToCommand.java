import java.util.*;
import java.io.*;

public class VerifyEdgesToCommand extends DirectedGraphTestCommand {
   protected String toLabel = "";
   protected ArrayList<String> fromLabels = new ArrayList<String>();

   public VerifyEdgesToCommand(String toVertexLabel, ArrayList<String> fromVertexLabels) {
      this.toLabel = toVertexLabel;
      this.fromLabels = new ArrayList<String>(fromVertexLabels);
   }

   @Override
   public boolean execute(PrintWriter testFeedback, DirectedGraph graph) {
      // Find toVertex
      Vertex toVertex = graph.getVertex(toLabel);
      if (toVertex == null) {
         testFeedback.write("FAIL: getVertex(\"" + toLabel + "\") returned ");
         testFeedback.write("null for a vertex that should exist\n");
         return false;
      }

      // Ask the graph for edges to toVertex
      ArrayList<Edge> actual = graph.getEdgesTo(toVertex);

      boolean pass = true;
      if (actual.size() == fromLabels.size()) {
         for (String fromLabel : fromLabels) {
            // Get the expected from-vertex
            Vertex expectedFrom = graph.getVertex(fromLabel);

            // If the actual ArrayList of vertices does not have the edge then the
            // test fails
            if (!hasEdge(actual, expectedFrom, toVertex)) {
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
      testFeedback.write(": Get edges to \"" + toLabel + "\"\n");
      printEdges(testFeedback, actual, ", ", "  Actual:   {", "}\n");
      testFeedback.write("  Expected: {");
      if (fromLabels.size() != 0) {
         testFeedback.write(fromLabels.get(0) + " to " + toLabel);
         for (int i = 1; i < (int) fromLabels.size(); i++) {
            testFeedback.write(", " + fromLabels.get(i) + " to " + toLabel);
         }
      }
      testFeedback.write("}\n");

      return pass;
   }
}
