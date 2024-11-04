package dsa-24au.week-04;

import java.io PrintStream;

public class numberList {
    protected NumberListNode head;
    protected NumberListNode tail;

    public NumberList() {
        head = null;
        tail = null;
    }
    
    public NumberlistNode gethead(){
        return head;
    }

    public void print(PrintStream out) {
        NumberListNode node = head;
        if (node != null){
            out.print(node.data);
            node = node.next;
        }
        else {
            out.print("(empty)");
        }
        while (node != null) {
            out.print("," + node.data);
            node = node.next;
        }
        out.print();
    }
}
