public class Main {

    public static void main(String[] args) {
        PrefixTree pt = new PrefixTree();
        System.out.println(pt);
        pt.lookupAndInsert("banana");
        int result = pt.lookup("banana");
        assert(result == 6);
        pt.lookupAndInsert("banner");
        System.out.println(pt);

        int result2 = pt.lookup("banan");
        assert(result2 == 5);
    }
}
