class Solution {
    public String intToRoman(int num) {
        String output = "";
        int[] vals = {1000, 500, 100, 50, 10, 5, 1};
        for (int i = 0; i < vals.length; i++) {
            if (num < vals[i]) {
                continue;
            }
            int fd = firstDigit(num);
            if (i > 0 && (fd == 4 || fd == 9)) {
                int downsteps = 0;
                if (i == 1 || i == 3 || i == 5) {
                    downsteps = 1;
                }
                output += String.valueOf(intToChar(vals[i+downsteps]));
                output += String.valueOf(intToChar(vals[i-1]));
                num = num - (vals[i-1] - vals[i+downsteps]);
            }
            if (num < vals[i]) {
                continue;
            }
            int reps = num / vals[i];
            output += String.valueOf(intToChar(vals[i])).repeat(reps);
            num = num % vals[i];
        }
        return output;
    }
    int firstDigit(int x) {
        while (x > 9) {
            x = x / 10;
        }
        return x;
    }
    public char intToChar(int num) {
        switch (num) {
        case 1:
            return 'I';
        case 5:
            return 'V';
        case 10:
            return 'X';
        case 50:
            return 'L';
        case 100:
            return 'C';
        case 500:
            return 'D';
        case 1000:
            return 'M';
        }
        return '0';
    }
}
