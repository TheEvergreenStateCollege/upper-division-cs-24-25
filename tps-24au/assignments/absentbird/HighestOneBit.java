class HighestOneBit {
    public static int findComplement(int num) {
        int mask = (Integer.highestOneBit(num) << 1) - 1;
        return num ^ mask;
    }
    public static void main(String args[]) {
    int input = 5;
    if (args.length > 0) {
        input = Integer.parseInt(args[0]);
    }
	int output = findComplement(input);
	System.out.println(output);
    }
}
