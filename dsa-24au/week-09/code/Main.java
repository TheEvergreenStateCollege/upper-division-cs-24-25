import java.util.*;
import java.io.*;

public class Main {
   public static void main(String[] args) {
      PrintWriter testFeedback = new PrintWriter(System.out);

      // Test AdjacencyListGraph first
      AdjacencyListGraph graph1 = new AdjacencyListGraph();
      System.out.println("AdjacencyListGraph:   ");
      boolean adjPass = testGraph(testFeedback, graph1);
      testFeedback.flush();

      // Test AdjacencyMatrixGraph second
      AdjacencyMatrixGraph graph2 = new AdjacencyMatrixGraph();
      System.out.println();
      System.out.println("AdjacencyMatrixGraph:");
      boolean matPass = testGraph(testFeedback, graph2);
      testFeedback.flush();

      // Print test results
      System.out.println();
      System.out.println("Summary:");
      System.out.print("  AdjacencyListGraph:   ");
      System.out.println(adjPass ? "PASS" : "FAIL");
      System.out.print("  AdjacencyMatrixGraph: ");
      System.out.println(matPass ? "PASS" : "FAIL");

      testFeedback.close();
   }

   public static boolean testGraph(PrintWriter testFeedback, DirectedGraph graph) {
      ArrayList<DirectedGraphTestCommand> commands = new ArrayList<>() {
         {
            add(new AddVertexCommand("A", true));
            add(new AddVertexCommand("B", true));

            // Verify that vertices A and B exist, but not C, D, or E
            add(new GetVertexCommand("C", false));
            add(new GetVertexCommand("A", true));
            add(new GetVertexCommand("B", true));
            add(new GetVertexCommand("E", false));
            add(new GetVertexCommand("D", false));

            // Add remaining vertices
            add(new AddVertexCommand("C", true));
            add(new AddVertexCommand("D", true));
            add(new AddVertexCommand("E", true));

            // Add edges
            add(new AddEdgeCommand("B", "C", true));
            add(new AddEdgeCommand("C", "A", true));
            add(new AddEdgeCommand("C", "D", true));
            add(new AddEdgeCommand("C", "E", true));
            add(new AddEdgeCommand("D", "C", true));
            add(new AddEdgeCommand("E", "A", true));
            add(new AddEdgeCommand("E", "D", true));

            // Attempts to add a duplicate edge should fail
            add(new AddEdgeCommand("C", "E", false));
            add(new AddEdgeCommand("D", "C", false));

            add(new VerifyEdgesFromCommand("A", (new ArrayList<String>(Arrays.asList()))));
            add(new VerifyEdgesFromCommand("B", (new ArrayList<String>(Arrays.asList("C")))));
            add(new VerifyEdgesFromCommand("C", (new ArrayList<String>(Arrays.asList("A", "D", "E")))));
            add(new VerifyEdgesFromCommand("D", (new ArrayList<String>(Arrays.asList("C")))));
            add(new VerifyEdgesFromCommand("E", (new ArrayList<String>(Arrays.asList("A", "D")))));

            add(new VerifyEdgesToCommand("A", (new ArrayList<String>(Arrays.asList("C", "E")))));
            add(new VerifyEdgesToCommand("B", (new ArrayList<String>(Arrays.asList()))));
            add(new VerifyEdgesToCommand("C", (new ArrayList<String>(Arrays.asList("B", "D")))));
            add(new VerifyEdgesToCommand("D", (new ArrayList<String>(Arrays.asList("C", "E")))));
            add(new VerifyEdgesToCommand("E", (new ArrayList<String>(Arrays.asList("C")))));

            // Verify some edges
            add(new HasEdgeCommand("A", "C", false));
            add(new HasEdgeCommand("A", "E", false));
            add(new HasEdgeCommand("B", "C", true));
            add(new HasEdgeCommand("C", "A", true));
            add(new HasEdgeCommand("C", "B", false));
            add(new HasEdgeCommand("C", "D", true));
            add(new HasEdgeCommand("C", "E", true));
            add(new HasEdgeCommand("D", "C", true));
            add(new HasEdgeCommand("E", "A", true));
            add(new HasEdgeCommand("E", "C", false));
            add(new HasEdgeCommand("E", "D", true));
         }
      };

      // Execute each test command, stopping if any command fails
      for (DirectedGraphTestCommand command : commands) {
         boolean pass = command.execute(testFeedback, graph);
         if (!pass) {
            return false;
         }
      }

      return true;
   }
}
