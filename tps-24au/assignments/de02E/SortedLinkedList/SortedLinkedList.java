public class SortedLinkedList {
    NumberListNode head;
    NumberListNode tail;
    NumberListNode current;

    public static void insertSorted(double newValue) {
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
                node.prev = current.prev;
                current.prev.next = node;
                current.prev = node;

            }
        }
    }

    public static void main(String[] arg) {

    }
}

