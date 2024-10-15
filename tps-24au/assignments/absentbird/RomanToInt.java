class Solution {
    public int romanToInt(String s) {        
        int total = 0;
        int last = 0;
        boolean sub = false;
        for (int i = s.length()-1; i > -1; i--) {
            int val = charToInt(s.charAt(i));
            if (val < last) {
                total += val * -1;
                sub = true;
            } else {
                total += val;
            }
            last = val;
        }
        return total;
    }
    public int charToInt(char c) {
        switch(c) {
        case 'I':
            return 1;
        case 'V':
            return 5;
        case 'X':
            return 10;
        case 'L':
            return 50;
        case 'C':
            return 100;
        case 'D':
            return 500;
        case 'M':
            return 1000;
        }
        return 0;
    }
}

