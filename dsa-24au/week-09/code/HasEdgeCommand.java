import java.io.*;

// Command that verifies the return value from a call to HasEdge()
public class HasEdgeCommand extends DirectedGraphTestCommand {
   protected String fromLabel = "";
   protected String toLabel = "";
   protected boolean expected;

   public HasEdgeCommand(String fromVertexLabel, String toVertexLabel, boolean expectedReturnValue) {
      fromLabel = fromVertexLabel;
      toLabel = toVertexLabel;
      expected = expectedReturnValue;
   }

   @Override
   public boolean execute(PrintWriter testFeedback, DirectedGraph graph) {
      // Find both vertices
      Vertex fromVertex = graph.getVertex(fromLabel);
      Vertex toVertex = graph.getVertex(toLabel);

      // Call HasEdge() to get the actual return value
      boolean actual = graph.hasEdge(fromVertex, toVertex);

      if (actual != expected) {
         testFeedback.write("FAIL: hasEdge() should have returned ");
         testFeedback.write((expected ? "true" : "false") + " for an edge from ");
         testFeedback.write((fromVertex != null ? fromVertex.getLabel() : "null"));
         testFeedback.write(" to ");
         testFeedback.write((toVertex != null ? toVertex.getLabel() : "null"));
         testFeedback.write(", but instead returned ");
         testFeedback.write((actual ? "true" : "false") + "\n");
         return false;
      }

      testFeedback.write("PASS: hasEdge() returned ");
      testFeedback.write((expected ? "true" : "false") + " for an edge from ");
      testFeedback.write((fromVertex != null ? fromVertex.getLabel() : "null"));
      testFeedback.write(" to ");
      testFeedback.write((toVertex != null ? toVertex.getLabel() : "null"));
      testFeedback.write("\n");
      return true;
   }
}
