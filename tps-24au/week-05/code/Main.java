public class Main {

    public static void main(String[] args) {
        PrefixTree pt = new PrefixTree();
        pt.lookupAndInsert("banana");
        int result = pt.lookup("banana");
        assert(result == 6);
        int result2 = pt.lookup("banan");
        assert(result2 == 5);
    }
}
