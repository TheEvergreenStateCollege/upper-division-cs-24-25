public class HighestOneBit {

    public static int highestOneBit(int x) {
        // >>> is "unsigned right shift" in Java 
        return x;
    }

    public void instanceMethod() {
        System.out.println("this " + this);
    }

    public static void main(String[] args) {
        HighestOneBit hob = new HighestOneBit();
        hob.instanceMethod();
        int result = highestOneBit(5);
        assert result == 4;
        System.out.println("highestOneBit(5) " + result);
    }
}