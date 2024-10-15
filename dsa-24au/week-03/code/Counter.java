public class Counter {
    private int count;                                // a simple integer instance variable
    public Counter() { }                                // default constructor (count is 0)
    public Counter(int initial) { count = initial; }            // an alternate constructor
    public int getCount() { return count; }                           // an accessor method
    public void increment() { count++; }                                // an update method
    public void increment(int delta) { count += delta; }                // an update method
    public void reset() { count = 0; }                                  // an update method
}