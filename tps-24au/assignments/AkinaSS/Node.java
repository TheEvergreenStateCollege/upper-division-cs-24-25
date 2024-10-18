public class Node<T> {
    public T data;
    Node<T> next;
    Node(T data) {
        this.data = data;
        this.next = null;
    }
}
