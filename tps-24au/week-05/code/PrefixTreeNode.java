import java.util.HashMap;
import java.util.Map;

public class PrefixTreeNode {

    // Traverse
    PrefixTreeNode parent;

    Map<Character,PrefixTreeNode> children = new HashMap<>();

    public PrefixTreeNode(PrefixTreeNode parent) {
        if (parent == null) {
            throw new RuntimeException("PrefixTreeNode parent cannot be null.");
        }
        this.parent = parent;
    }

    // We only allow our RootPrefixTreeNode subclass to instantiate us this way
    protected PrefixTreeNode() {
        this.parent = null;
    }

    public PrefixTreeNode getChild(char c) {
        return this.children.get(c);
    }

    /**
     *
     * @param suffix remaining substring to insert starting from this PrefixTreeNode, after this PrefixTreeNode's incoming edge letter
     * @return true if inserting this suffix string resulted in any new PrefixTreeNodes being inserted into the subtree rooted at this PrefixTreeNode.
     */
    public boolean insertChild(String suffix) {
        if (suffix.length() == 0) {
            return false;
        }
        char c = suffix.charAt(0);

        boolean inserted = false;
        PrefixTreeNode n;
        if (children.containsKey(c)) {
            n = children.get(c);
            inserted = n.insertChild(suffix.substring(1));            
        } else {
            n = new PrefixTreeNode(this);
            children.put(c, n);
            inserted = n.insertChild(suffix.substring(1));
            System.out.println(suffix);
        }
        return inserted;
    }

    /**
     * Returns distance from root (for indentation in toString).
     * Root has height 0, every other node has height 1 + its parent height.
     * @return the height
     */
    public int getHeight() {
        if (this.parent == null) {
            return 0;
        }
        return this.parent.getHeight() + 1;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        StringBuilder indent = new StringBuilder();
        indent.append("|");
        for (int i = 0; i < getHeight(); i++) {
            indent.append("  ");
        }
        for (Map.Entry<Character,PrefixTreeNode> entry : this.children.entrySet()) {
            sb.append(indent + entry.getKey().toString() + "\n");
            sb.append(indent + entry.getValue().toString() + "\n");
        }
        return sb.toString();
    }
}


