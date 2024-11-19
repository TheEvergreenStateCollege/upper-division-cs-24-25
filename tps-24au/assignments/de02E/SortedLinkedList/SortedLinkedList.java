public class SortedLinkedList {
    NumberListNode head;
    NumberListNode tail;

    public void insertSorted(double newValue) {
        NumberListNode current;

        NumberListNode node = new NumberListNode(newValue);
        if (head == null && tail == null) {
            head = node;
            tail = node;
            return;
        }
        current = head;
        while (current != null) {
            if (current.value > newValue) {
                node.next = current;
                if (current == this.head) {
                    this.head = node;
                } else {
                    node.prev = current.prev;
                    current.prev.next = node;
                    current.prev = node;
                }
                return;
            }
            current = current.next;
        }
        node.prev = tail;
        tail.next = node;
        tail = node;
    }

    public static void main(String[] arg) {

    }
}

