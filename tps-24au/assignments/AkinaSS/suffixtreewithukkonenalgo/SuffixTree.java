package suffixtreewithukkonenalgo;

public class SuffixTree {
    // Define all the necessary data structures (Nodes, Edges, etc.) as per the previous code.
    static char[] text;
    static SuffixTreeNode root;
    static SuffixTreeNode lastNewNode;
    static SuffixTreeNode activeNode;
    static int count;
    static int activeEdge = -1;
    static int activeLength = 0;
    static int remainingSuffixCount = 0;
    static int leafEnd = -1;
    static int[] rootEnd;
    static int[] splitEnd;
    static int size = -1;

    public static SuffixTreeNode newNode(int start, int[] end) {
        count++;
        SuffixTreeNode node = new SuffixTreeNode();
        for (int i = 0; i < 265; i++) {
            node.children[i] = null;
        }
        node.suffixLink = root;
        node.start = start;
        node.end = end;
        node.suffixIndex = -1;
        return node;
    }

    public static int edgeLength(SuffixTreeNode n) {
        return n.end[0] - n.start + 1;
    }

    public static boolean walkDown(SuffixTreeNode currNode) {
        if (activeLength >= edgeLength(currNode)) {
            activeEdge = text[size - remainingSuffixCount + 1] - ' ';
            activeLength -= edgeLength(currNode);
            return true;
        }
        return false;
    }

    public static void extendSuffixTree(int pos) {
        leafEnd = pos;
        remainingSuffixCount++;
        lastNewNode = null;

        while (remainingSuffixCount > 0) {
            if (activeLength == 0) {
                activeEdge = text[pos] - ' ';
            }

            if (activeNode.children[activeEdge] == null) {
                activeNode.children[activeEdge] = newNode(pos, new int[] { leafEnd });

                if (lastNewNode != null) {
                    lastNewNode.suffixLink = activeNode;
                    lastNewNode = null;
                }
            }
            else {
                SuffixTreeNode next = activeNode.children[activeEdge];
                if (walkDown(next)) {
                    continue;
                }

                if (text[next.start + activeLength] == text[pos]) {
                    if (lastNewNode != null && activeNode != root) {
                        lastNewNode.suffixLink = activeNode;
                        lastNewNode = null;
                    }

                    activeLength++;
                    break;
                }
                splitEnd = new int[] {next.start + activeLength - 1};
                SuffixTreeNode split = newNode(next.start, splitEnd);
                activeNode.children[activeEdge] = split;
                split.children[text[pos] - ' '] = newNode(pos, new int[] {leafEnd});
                next.start = activeLength;
                split.children[activeEdge] = next;

                if (lastNewNode != null) {
                    lastNewNode.suffixLink = split;
                }

                lastNewNode = split;
            }

            remainingSuffixCount--;
            if (activeNode == root && activeLength > 0) {
                activeLength--;
                activeEdge = text[pos - remainingSuffixCount + 1] - ' ';
            }
            else if (activeNode != root) {
                activeNode = activeNode.suffixLink;
            }
        }
    }

    public static void print(int i, int j) {
        for (int k = i; k <= j; k++) {
            System.out.print(text[k]);
        }
    }

    public static void setSuffixIndexByDFS(SuffixTreeNode n, int labelHeight) {
        if (n == null) {
            return;
        }

        if (n.start != -1) {
            print(n.start, n.end[0]);
        }

        int leaf = 1;
        for (int i = 0; i < 256; i++) {
            if (n.children[i] != null) {
                if (leaf == 1 && n.start != -1) {
                    System.out.println("[" + n.suffixIndex + "]");
                }

                leaf = 0;
                setSuffixIndexByDFS(n.children[i], labelHeight + edgeLength(n.children[i]));
            }
        }
        if (leaf == 1) {
            n.suffixIndex = size - labelHeight;
            System.out.println("[" + n.suffixIndex + "]");
        }
    }

    public static void freeSuffixTreeByPostOrder(SuffixTreeNode n) {
        if (n == null) {
            return;
        }

        for (int i = 0; i < 265; i++) {
            if (n.children[i] != null) {
                freeSuffixTreeByPostOrder(n.children[i]);
            }
        }
        if(n.suffixIndex == -1) {
            n.end = null;
        }
    }

    public static void buildSuffixTree() {
        size = text.length;
        rootEnd = new int[1];
        rootEnd[0] = -1;

        root = newNode(-1, rootEnd);

        activeNode = root;
        for (int i = 0; i < size; i++) {
            extendSuffixTree(i);
        }
        int labelHeight = 0;
        setSuffixIndexByDFS(root, labelHeight);

        freeSuffixTreeByPostOrder(root);
    }

    // Main function to demonstrate usage
    public static void main(String[] args) {
        text = "abbc".toCharArray();
        buildSuffixTree();
        System.out.println("Number of nodes in suffix tree are " + count);
    }
}