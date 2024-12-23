// This prefix tree is hardcoded to support characters and strings
public class PrefixTree {

    /**
     * The root is a special singleton subclass of PrefixTreeNode
     * with no edge letter, representing the empty string.
     */
    public static class RootNode extends PrefixTreeNode {

        public RootNode() {
            super();
            // Root PrefixTreePrefixTreeNode is the only one allowed
        }

    }

    PrefixTreeNode root;

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
        PrefixTreeNode curr = this.root;
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
        return "PrefixTree: " + this.root.toString();
    }

    // Find the longest repeating substring by traversing the tree
    public String findLongestRepeatingSubstring() {
        return findLongestRepeatingSubstringHelper(this.root, 0, "");
    }

    private String findLongestRepeatingSubstringHelper(PrefixTreeNode node, int depth, String path) {
        String longest = "";
        if (node.count > 1 && depth > longest.length()) {
            longest = path;
        }

        for (PrefixTreeNode child : node.children.values()) {
            String childLongest = findLongestRepeatingSubstringHelper(child, depth + 1, path + child.getPath());
            if (childLongest.length() > longest.length()) {
                longest = childLongest;
            }
        }
        return longest;
    }


}
