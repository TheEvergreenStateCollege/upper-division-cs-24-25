package LongestRepeatingSubsInGeneral;
import java.util.*;

public class LRSwithSuffixFromC {
    static final int MAX_CHAR = 256;  // Maximum number of characters
    static String text;  // Input string
    static Node root = null;  // Pointer to root node

    static Node lastNewNode = null;
    static Node activeNode = null;

    static int activeEdge = -1;
    static int activeLength = 0;

    static int remainingSuffixCount = 0;
    static int leafEnd = -1;
    static int rootEnd = -1;
    static int size = -1;

    static Node newNode(int start, int end) {
        Node newNode = new Node(start, end);
        for (int i = 0; i < MAX_CHAR; i++) {
            newNode.children[i] = null;
        }
        newNode.suffixLink = root;
        newNode.suffixIndex = -1;
        return newNode;
    }

    static int edgeLength(Node node) {
        if (node == root) {
            return 0;
        }
        return node.end - node.start + 1;
    }

    static boolean walkDown(Node currNode) {
        if (activeLength >= edgeLength(currNode)) {
            activeEdge += edgeLength(currNode);
            activeLength -= edgeLength(currNode);
            activeNode = currNode;
            return true;
        }
        return false;
    }

    static void extendSuffixTree(int pos) {
        leafEnd = pos;
        remainingSuffixCount++;
        lastNewNode = null;

        while (remainingSuffixCount > 0) {
            if (activeLength == 0) {
                activeEdge = pos;
            }

            if (activeNode.children[activeEdge] == null) {
                activeNode.children[activeEdge] = newNode(pos, leafEnd);

                if (lastNewNode != null) {
                    lastNewNode.suffixLink = activeNode;
                    lastNewNode = null;
                }
            }
            else {
                Node next = activeNode.children[activeEdge];
                if (walkDown(next)) {
                    continue;
                }
                if (text.charAt(next.start + activeLength) == text.charAt(pos)) {
                    if ((lastNewNode != null) && (activeNode != root)) {
                        lastNewNode.suffixLink = activeNode;
                        lastNewNode = null;
                    }
                    activeLength++;
                    break;
                }

                int splitEnd = next.start + activeLength - 1;
                Node split = newNode(next.start, splitEnd);
                activeNode.children[activeEdge] = split;

                split.children[activeEdge] = newNode(pos, leafEnd);
                next.start += activeLength;
                split.children[activeEdge] = next;

                if (lastNewNode != null) {
                    lastNewNode.suffixLink = split;
                }
                lastNewNode = split;
            }

            remainingSuffixCount--;
            if (activeNode == root && activeLength > 0) {
                activeLength--;
                activeEdge = pos - remainingSuffixCount + 1;
            }
            else if (activeNode != root) {
                activeNode = activeNode.suffixLink;
            }
        }
    }

    static void print(int i, int j) {
        for (int k = i; k <= j; k++) {
            System.out.println(text.charAt(k));
        }    
    }

    static void setSuffixIndexByDFS(Node n, int labelHeight) {
        if (n == null) {
            return;
        }

        if (n.start != -1) {
            print(n.start, n.end);
        }

        int leaf = 1;
        for (int i = 0; i < MAX_CHAR; i++) {
            if (n.children[i] != null) {
                leaf = 0;
                setSuffixIndexByDFS(n.children[i], labelHeight + edgeLength(n.children[i]));
            }
        }
        if (leaf == 1) {
            n.suffixIndex = size - labelHeight;
        }
    }

    static void freeSuffixTreeByPostOrder(Node n) {
        if (n == null) {
            return;
        }
        for (int i = 0; i < MAX_CHAR; i++) {
            if (n.children[i] != null) {
                freeSuffixTreeByPostOrder(n.children[i]);
            }
        }
    }

    static void buildSuffixTree() {
        size = text.length();
        rootEnd = -1;
        root = newNode(-1, rootEnd);
  
        activeNode = root;
        for (int i = 0; i < size; i++) {
            extendSuffixTree(i);
        }
        
        int labelHeight = 0;
        setSuffixIndexByDFS(root, labelHeight);
    }

    static void doTraversal(Node n, int labelHeight, int maxHeight, int substringStartIndex) {
        if(n == null) {
            return;
        }
        if(n.suffixIndex == -1) {
            for (int i = 0; i < MAX_CHAR; i++) {
                if(n.children[i] != null) {
                    doTraversal(n.children[i], labelHeight + edgeLength(n.children[i]), maxHeight, substringStartIndex);
                }
            }
        }
        else if(n.suffixIndex > -1 && (maxHeight < labelHeight - edgeLength(n))) {
            maxHeight = labelHeight - edgeLength(n);
            substringStartIndex = n.suffixIndex;
        }
    }

    static void getLongestRepeatedSubstring() {
        int maxHeight = 0;
        int substringStartIndex = 0;
        doTraversal(root, 0, maxHeight, substringStartIndex);
        // System.out.printf("maxHeight %d, substringStartIndex %d\n", maxHeight, substringStartIndex);
        System.out.printf("Longest Repeated Substring in %s is: ", text);
        for (int k = 0; k < maxHeight; k++) {
            System.out.println(text.charAt(k + substringStartIndex));

            if(k == 0) {
                System.out.println("No repeated substring");
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        while (sc.hasNextLine()) {
            text = sc.nextLine();
            buildSuffixTree();
            getLongestRepeatedSubstring();
            freeSuffixTreeByPostOrder(root);
        }
        sc.close();
    //     text = "banana"; 
    //     buildSuffixTree();    
    //     getLongestRepeatedSubstring();
    // //Free the dynamically allocated memory
    //     freeSuffixTreeByPostOrder(root);
    }
}
