import java.io.*;

// Command that adds a new vertex to the graph and verifies that the addition
// either failed or succeeded
public class AddVertexCommand extends DirectedGraphTestCommand {
   protected String label = "";
   protected boolean shouldSucceed;

   public AddVertexCommand(String vertexLabel, boolean shouldSucceed) {
      this.label = vertexLabel;
      this.shouldSucceed = shouldSucceed;
   }

   @Override
   public boolean execute(PrintWriter testFeedback, DirectedGraph graph) {
      // Try to add the vertex. If the return value is non-null, then addition
      // is successful, otherwise addition has failed.
      Vertex newVertex = graph.addVertex(label);

      if (newVertex != null) {
         if (!shouldSucceed) {
            testFeedback.write("FAIL: addVertex(\"" + label + "\") returned ");
            testFeedback.write("non-null, but should have returned ");
            testFeedback.write("null due to the label already being in ");
            testFeedback.write("use" + "\n");
            return false;
         }

         testFeedback.write("PASS: addVertex(\"" + label + "\") returned ");
         testFeedback.write("non-null" + "\n");
         return true;
      }

      if (shouldSucceed) {
         testFeedback.write("FAIL: addVertex(\"" + label + "\") returned ");
         testFeedback.write("null, but should have returned non-null ");
         testFeedback.write("\n");
         return false;
      }

      testFeedback.write("PASS: addVertex(\"" + label + "\") returned null ");
      testFeedback.write("because the label is already in use" + "\n");
      return true;
   }
}
