package suffixtreewithukkonenalgo;
// Java Program to Implement Suffix Tree
// Beta version
/** Class Suffix Tree **/

class SuffixTreeNode {
    SuffixTreeNode[] children;
    SuffixTreeNode suffixLink;
    int start;
    int[] end;
    int suffixIndex;

    public SuffixTreeNode() {
        this.children = new SuffixTreeNode[256];
        this.suffixLink = null;
        this.start = 0;
        this.end = new int[1];
        this.suffixIndex = -1;
    }
}