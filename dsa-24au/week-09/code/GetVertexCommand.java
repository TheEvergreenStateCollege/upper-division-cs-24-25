import java.io.*;

// Command that gets a vertex by label and verifies the result
public class GetVertexCommand extends DirectedGraphTestCommand {
   protected String label = "";
   protected boolean shouldExist;

   public GetVertexCommand(String vertexLabel, boolean vertexShouldExist) {
      this.label = vertexLabel;
      shouldExist = vertexShouldExist;
   }

   @Override
   public boolean execute(PrintWriter testFeedback, DirectedGraph graph) {
      // Get the vertex by calling GetVertex()
      Vertex vertex = graph.getVertex(label);

      // Check if the returned vertex is non-null
      if (vertex != null) {
         // If the vertex shouldn't exist, then print a failure message
         if (!shouldExist) {
            testFeedback.write("FAIL: getVertex(\"" + label + "\") returned ");
            testFeedback.write("non-null, but should have returned ");
            testFeedback.write("null" + "\n");
            return false;
         }

         // Verify the vertex's label
         String actualLabel = vertex.getLabel();
         if (!label.equals(actualLabel)) {
            testFeedback.write("FAIL: getVertex(\"" + label + "\") returned a ");
            testFeedback.write("vertex with incorrect label \"" + actualLabel);
            testFeedback.write("\"" + "\n");
            return false;
         }

         testFeedback.write("PASS: getVertex(\"" + label + "\") returned a ");
         testFeedback.write("non-null vertex with a correct label" + "\n");
         return true;
      }

      // The returned vertex is null, so check if a null vertex is expected
      if (shouldExist) {
         testFeedback.write("FAIL: getVertex(\"" + label + "\") returned ");
         testFeedback.write("null, but should have returned non-null ");
         testFeedback.write("\n");
         return false;
      }

      // PASS
      testFeedback.write("PASS: getVertex(\"" + label + "\") returned ");
      testFeedback.write("null" + "\n");
      return true;
   }
}
