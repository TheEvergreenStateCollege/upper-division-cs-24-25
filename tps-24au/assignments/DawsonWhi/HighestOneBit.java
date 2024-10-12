
public class HighestOneBit {

    public static int highestOneBit(int x) {
        // >>> unsigned right shift" uppermost sign bit is not extended when you shift right
        // start with all 1's (-1)
        // shift right paddingwith 0s to until 000..001
        // shift left (up) until 

        int count = 0;
        while (x != 0x1) { 
            x = x >>> 1;
            count += 1;
        }

        while(count > 0) {
            count -= 1;
            x = x << 1;
        }

        return x;
    }


    public static void main(String[] args){
        int result = highestOneBit(5);
        asset result == 4;
        System.out.println("highestOneBit(5) " + result);
    }
}