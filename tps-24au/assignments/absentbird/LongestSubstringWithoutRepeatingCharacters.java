class Solution {
    public int lengthOfLongestSubstring(String s) {
        String longest = "";
        String current = "";
        int last = 0;
        for (int i = 0; i < s.length(); i++) {
            boolean unique = true;
            for (int j=0; j < current.length(); j++) {
                if (s.charAt(i) == current.charAt(j)) {
                    unique = false;
                    last = j;
                }
            }
            if (unique) {
                current += s.charAt(i);
            } else {
                if (current.length() > longest.length()) {
                    longest = current;
                }
                current = current.substring(last+1)+s.charAt(i);
            }
        }
        if (current.length() > longest.length()) {
            longest = current;
        }
        return longest.length();
    }
}

