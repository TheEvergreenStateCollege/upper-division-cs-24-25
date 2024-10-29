<<<<<<< HEAD
import java.io.PrintStream;

public class NumberList {
   protected NumberListNode head;
   protected NumberListNode tail;

   public NumberList() {
      head = null;
      tail = null;
   }

   public NumberListNode getHead() {
      return head;
   }

   // Prints the lists's contents in order from head to tail
   public void print(PrintStream out) {
      NumberListNode node = head;
      if (node != null) {
         // Head node is not preceded by separator
         out.print(node.data);
         node = node.next;
      }
      else {
         // Special case for empty list
         out.print("(empty)");
      }

      while (node != null) {
         out.print(", " + node.data);
         node = node.next;
      }

      out.println();
   }
}
=======
import java.io PrintStream;

public class NumberList{
    protected NumberListNode head;
    protected NumberListNode tail;

    public NumberList(){
        head = null;
        tail = null;
    }

    public NumberListNode gethead(){
        return head;
    }

    public void print(PrintStream out){
        NumberListNode node = head;
        if (node != null){
            //head node is not preceded by seperator
            out.print(node.data);
        }
        else {
            out.print("empty");
        }

        while(node != null){
        out.print("," + node.data);
        node = node.data;
        out.println();
        } 
    }
    
}
>>>>>>> 349d2abae5e57afe8c94487d465bf2be7bd189a9
