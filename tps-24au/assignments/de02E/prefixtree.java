import java.util.HashMap;
import java.util.Map;

// This prefix tree is hardcoded to support characters and strings
public class PrefixTree {

    public static class Node {

        // Traverse
        Node parent;

        Map<Character,Node> children = new HashMap<>();

        public Node(Node parent) {
            if (parent == null) {
                throw new RuntimeException("Node parent cannot be null.");
            }
            this.parent = parent;
        }

        // We only allow our RootNode subclass to instantiate us this way
        protected Node() {
            this.parent = null;
        }

        public Node getChild(char c) {
            return this.children.get(c);
        }

        /**
         *
         * @param suffix remaining substring to insert starting from this node, after this node's incoming edge letter
         * @return true if inserting this suffix string resulted in any new nodes being inserted into the subtree rooted at this node.
         */
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
                n.insertChild(suffix.substring(1));
                inserted = true;
            }
            return inserted || n.insertChild(suffix.substring(1));
        }

        public String toString() {
            StringBuilder sb = new StringBuilder();
            for ( Map.Entry<Character,Node> pair : this.children.entrySet()) {
                sb.append(pair.getKey()+": "+pair.getValue().toString()+"\n");
            }
            return sb.toString();
        }
    }

    /**
     * The root is a special singleton subclass of Node
     * with no edge letter, representing the empty string.
     */
    public static class RootNode extends Node {

        public RootNode() {
            super();
            // Root node is the only one allowed
        }

    }

    Node root;

    public PrefixTree() {
        this.root = new RootNode();
    }

    /**
     *
     * @param s
     * @return the index of the first letter not found in prefix tree,
     * where first character is zero
     */
    public int lookup(String s) {
        Node curr = this.root;
        for (int i = 0; (i < s.length()) && (curr != null); i += 1) {
            curr = curr.getChild(s.charAt(i));
            if (curr == null) {
                // we didn't reach end of string but reached a leaf in our prefix tree
                return i;
            }
        }
        return s.length();
    }

    /**
     * Return true if we had to insert this string
     * @param s
     * @return
     */
    public boolean lookupAndInsert(String s) {
        return this.root.insertChild(s);
    }

    public String toString() {
        return this.root.toString();
    }


}
