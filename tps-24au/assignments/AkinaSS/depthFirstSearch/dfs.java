public class dfs {
    public static boolean traverse(Node<T> head, T value) {
        if (head.data == value) {
            System.out.println(head.data);
            return true;
        }
        else if (head.next == null) {
            return false;
        }
        else {
            traverse(head.next, value);
        }
        return false;
    }
}
