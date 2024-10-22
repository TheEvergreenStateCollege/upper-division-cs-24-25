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
