class LongestRepeatingSubstring {
    public static String longestRepeatingSubstring(String s) {
        int half = s.length() / 2;
        for(int i = 0; i < s.length(); i++) {
            if (i % 2 == 1) {
                half--;
            }
            if (s.length() % 2 == 1) {
                if (i == 1) {
                    half ++;
                } else if (i == 2) {
                    half--;
                }
            }
            String candidate = s.substring(i, i + half);
            String next = s.substring(i + half, i + half * 2);
            if (candidate.equals(next)) {
                return candidate;
            }
        };
        return "";
    }
    public static void main(String []args) {
        String result = longestRepeatingSubstring(args[0]);
        System.out.println(result);
    }
}
