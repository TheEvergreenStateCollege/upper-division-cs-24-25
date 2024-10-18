public class CounterDemo {
    public static void main(String[] args) {
        Counter c;                  // declares a variable; no Counter instance created
        c = new Counter();          // constructs a Counter; assigns its reference to c
        c.increment();              // increases its count by 1
        c.increment(3);             // further increases its count by 3
        int temp = c.getCount();    // will be 4
        c.reset();                  // count becomes 0
        Counter d = new Counter(5); // declares and constructs a Counter with count 5
        d.increment();              // count becomes 6
        Counter e = d;              // assigns e to reference the same instance as d
        temp = e.getCount();        // will be 6 (as e and d reference the same Counter)
        e.increment(2);             // count of e (also known as d) becomes 8
    }
}