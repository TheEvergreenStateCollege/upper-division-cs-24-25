public class DFS<T>{

    /**
     * 
     * @param value - the value to search for
     * @param head - the first node of the linked list to traverse, 
     * @return true if the given value is found in any node of the linked list starting with head.
     */
    public static boolean search(Node<T> head, T value){
        if (head.value == value) {
            System.out.println(this.value);
            return true;
        } else if (head.next == null) {
            return false;
        } else {
            search(head.next, value);
        }
    }

        /**
     * 
     * @param value - the value to search for
     * @param head - the first node of the linked list to traverse, 
     * @return the "last" node (longest distance from the head) whose value matches the given parameter,
     * or null if the value is not found. 
     */
    public static Node<T> search(Node<T> head, T value){
        if (head.value == value) {
            return true;
        } else if (head.next == null) {
            return false;
        } else {
            search(head.next, value);
        }
    }

    public static void traverse(Node<T> head) {
        List<> visited = new ArrayList<T>();

        
        while (head != null) {
            if (!visited.contains(head)) {
                visited.add(head);
            }
            // Traverse down the left side as far as we can
            while (head != null && head.left != null) {
                head = head.left;
            }

            // 
        }
    }

    public static void main(String[] args) {
        Node a = new Node<int>(1);
        Node b = new Node<int>(2);
        Node c = new Node<int>(3);
        Node d = new Node<int>(4);

        a.next = b;
        b.next = c;
        c.next = d;

        traverse(a);
    }



}