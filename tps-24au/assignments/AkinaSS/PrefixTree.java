import java.util.HashMap;
import java.util.Map;

public class PrefixTree {

    public static class Node {
        Node parent;
        Map<Character, Node> children = new HashMap<>();
        int count = 0; // Track frequency of this node's substring

        public Node(Node parent) {
            if (parent == null) {
                throw new RuntimeException("Node parent cannot be null.");
            }
            this.parent = parent;
        }

        protected Node() {
            this.parent = null;
        }

        public Node getChild(char c) {
            return this.children.get(c);
        }

        public boolean insertChild(String suffix) {
            if (suffix.length() == 0) {
                return false;
            }
            char c = suffix.charAt(0);
            boolean inserted = false;
            Node n;
            if (children.containsKey(c)) {
                n = children.get(c);
            } else {
                n = new Node(this);
                children.put(c, n);
                inserted = true;
            }
            n.count++; // Increment the count when a new suffix is inserted through this node
            return inserted || n.insertChild(suffix.substring(1));
        }

        public String toString() {
            StringBuilder sb = new StringBuilder();
            for (Map.Entry<Character, Node> pair : this.children.entrySet()) {
                sb.append(pair.getKey() + ": " + pair.getValue().toString() + "\n");
            }
            return sb.toString();
        }

        // To get the string from this node
        public String getPath() {
            StringBuilder sb = new StringBuilder();
            Node curr = this;
            while (curr.parent != null) {
                for (Map.Entry<Character, Node> entry : curr.parent.children.entrySet()) {
                    if (entry.getValue() == curr) {
                        sb.insert(0, entry.getKey());
                        break;
                    }
                }
                curr = curr.parent;
            }
            return sb.toString();
        }
    }

    public static class RootNode extends Node {
        public RootNode() {
            super();
        }
    }

    Node root;

    public PrefixTree() {
        this.root = new RootNode();
    }

    public boolean lookupAndInsert(String s) {
        return this.root.insertChild(s);
    }

    public String toString() {
        return this.root.toString();
    }

    // Find the longest repeating substring by traversing the tree
    public String findLongestRepeatingSubstring() {
        return findLongestRepeatingSubstringHelper(this.root, 0, "");
    }

    private String findLongestRepeatingSubstringHelper(Node node, int depth, String path) {
        String longest = "";
        if (node.count > 1 && depth > longest.length()) {
            longest = path;
        }

        for (Node child : node.children.values()) {
            String childLongest = findLongestRepeatingSubstringHelper(child, depth + 1, path + child.getPath());
            if (childLongest.length() > longest.length()) {
                longest = childLongest;
            }
        }
        return longest;
    }

    public static void main(String[] args) {
        PrefixTree tree = new PrefixTree();

        // Example string, add all suffixes
        String s = "banana$";
        for (int i = 0; i < s.length(); i++) {
            tree.lookupAndInsert(s.substring(i));
        }

        // Find the longest repeated substring
        String result = tree.findLongestRepeatingSubstring();
        System.out.println("Longest Repeating Substring: " + result);
    }
}

