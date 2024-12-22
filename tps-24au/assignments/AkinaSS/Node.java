import java.util.Arrays;

public class Node {
    Node[] children = new Node[LRSwithSuffixFromC.MAX_CHAR];
    Node suffixLink;
    int start;
    int end;
    int suffixIndex;

    Node(int start, int end) {
        Arrays.fill(children, null);
        this.suffixLink = null;
        this.start = start;
        this.end = end;
        this.suffixIndex = -1;
    }
}