import java.io.*;

// Command that adds an edge to a graph
public class AddEdgeCommand extends DirectedGraphTestCommand {
   protected String fromLabel = "";
   protected String toLabel = "";
   protected boolean shouldSucceed;

   public AddEdgeCommand(String fromVertexLabel, String toVertexLabel, boolean shouldSucceed) {
      fromLabel = fromVertexLabel;
      toLabel = toVertexLabel;
      this.shouldSucceed = shouldSucceed;
   }

   @Override
   public boolean execute(PrintWriter testFeedback, DirectedGraph graph) {
      // Find both vertices
      Vertex fromVertex = graph.getVertex(fromLabel);
      Vertex toVertex = graph.getVertex(toLabel);

      // Add the edge
      boolean addedEdge = false;
      if (fromVertex != null && toVertex != null) {
         addedEdge = graph.addDirectedEdge(fromVertex, toVertex);
      }

      if (addedEdge == shouldSucceed) {
         // PASS
         testFeedback.write("PASS: ");
         if (addedEdge) {
            testFeedback.write("Added edge from \"" + fromLabel + "\" to \"");
            testFeedback.write(toLabel + "\"" + "\n");
         }
         else {
            testFeedback.write("Attempt to add edge from \"" + fromLabel);
            testFeedback.write("\" to \"" + toLabel + "\" returned false");
            testFeedback.write("\n");
         }
         return true;
      }

      // FAIL
      testFeedback.write("FAIL: Add edge from \"" + fromLabel + "\" to \"");
      testFeedback.write(toLabel + "\"" + "\n");
      return false;
   }
}
