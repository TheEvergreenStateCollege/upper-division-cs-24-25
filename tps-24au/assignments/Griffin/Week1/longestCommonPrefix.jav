class Solution {
    public String longestCommonPrefix(String[] strs) {
        String sample = strs[0];
        String longestCommonPrefix = "";

        //for each char in sample
        for (int i = 0; i < sample.length(); ++i) {
            //for each string in array
            for (int j = 1; j < strs.length; ++j) {
                if (i >= strs[j].length() || sample.charAt(i) != strs[j].charAt(i)) {
                    return longestCommonPrefix;
                }

            }
            longestCommonPrefix += sample.charAt(i);
        }
        return longestCommonPrefix;
    }
}