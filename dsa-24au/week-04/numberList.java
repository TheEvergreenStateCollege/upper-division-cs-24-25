import java.util.*;
import java.io PrintStream ();

public class NumberList{
    protected NumberListNode head;
    protected NumberListNode tail;
    
        public NUmberList (){
            head = null;
            tail = null;
        }
        
    public NumberListNode getHead(){
        return head;
    }
    public void print (PrintStream out){
        NUmberListNode node = head;
        if(node != null){
            System.out.print(node.data);
            node = node.next();
        }
        else{
            System.out.print("empty");
        }
        while (node != null){
            out.print("," + node.data);
            node = node.next;
        }
        out.println();
    }
}
