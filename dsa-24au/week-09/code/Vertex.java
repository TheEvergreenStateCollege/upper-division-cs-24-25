import java.io.*;

public class Vertex {
   protected String label;

   public Vertex(String vertexLabel) {
      label = vertexLabel;
   }

   public String getLabel() {
      return label;
   }

   public void setLabel(String newLabel) {
      label = newLabel;
   }

   // Prints this vertex's label
   public void print(PrintWriter output) {
      output.write(label);
   }
}
