import java.util.HashMap;
import java.util.Map;

public class SuffixTreeBuilder {
    private final String text; // Input string
    private final Node root;   // Root node of the suffix tree

    public SuffixTreeBuilder(String text) {
        this.text = text + "$"; // Append unique end character to ensure suffix uniqueness
        this.root = new Node(); // Initialize the root node
    }

    // Builds the suffix tree for the input string
    public Node build() {
        for (int i = 0; i < text.length(); i++) {
            addSuffix(i);
        }
        return root;
    }

    // Adds a suffix starting from position 'start' to the tree
    private void addSuffix(int start) {
        Node current = root;
        for (int i = start; i < text.length(); i++) {
            char c = text.charAt(i);
            if (!current.hasChild(c)) {
                // Create a new leaf node for the suffix
                Node leaf = new Node(i, text.length());
                current.addChild(c, leaf);
                return;
            } else {
                // Traverse down to the child node
                current = current.getChild(c);
            }
        }
    }

    // Print the suffix tree for debugging
    public void printTree(Node node, String prefix) {
        for (Map.Entry<Character, Node> entry : node.children.entrySet()) {
            char c = entry.getKey();
            Node child = entry.getValue();

            // Print edge label
            System.out.println(prefix + "-> " + text.substring(child.start, child.end));
            printTree(child, prefix + "  ");
        }
    }

    public class Node {
        // Stores edges to child nodes
        Map<Character, Node> children = new HashMap<>();

        // Tracks the start and end of the edge label in the input string
        int start;
        int end;

        public Node() {
            this.start = -1; 
            this.end = -1;
        }

        // Constructor for leaf nodes
        public Node(int start, int end) {
            this.start = start;
            this.end = end;
        }

        public void addChild(char c, Node node) {
            children.put(c, node);
        }

        public boolean hasChild(char c) {
            return children.containsKey(c);
        }

        public Node getChild(char c) {
            return children.get(c);
        }
        // Believe it or not this prints the tree
        public void printTree(Node node, String prefix) {
            for (Map.Entry<Character, Node> entry : node.children.entrySet()) {
                char c = entry.getKey();
                Node child = entry.getValue();

                System.out.println(prefix + text.substring(child.start, child.end));
                printTree(child, prefix + "  ");
            }
        }
    }


    public static void main(String[] args) {
        // Example usage
        String input = "banana";
        SuffixTreeBuilder builder = new SuffixTreeBuilder(input);

        Node root = builder.build();
        builder.printTree(root, "");
    }
        public static void Main(String[] args) {
            // Example input
            String input = "banana";
    
            // Build the suffix tree
            SuffixTreeBuilder builder = new SuffixTreeBuilder(input);
            Node root = builder.build();
    
            // Print the suffix tree
            System.out.println("Suffix Tree for \"" + input + "\":");
            builder.printTree(root, "");
        }
}
