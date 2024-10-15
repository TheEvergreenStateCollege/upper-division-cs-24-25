class Solution {
    public String longestCommonPrefix(String[] strs) {
        String common = "";
        for (int i = 0; i < strs.length; i++) {
            if (i == 0) {
                common = strs[i];
                continue;
            }
            if (common.length() == 0 || strs[i].length() == 0) {
                common = "";
                break;
            }
            if (common.charAt(0) != strs[i].charAt(0)) {
                common = "";
                break;
            }
            if (common.length() > strs[i].length()) {
                common = common.substring(0, strs[i].length());
            }
            for (int j = 0; j < common.length(); j++) {
                if (common.charAt(j) != strs[i].charAt(j)) {
                    common = common.substring(0, j);
                    break;
                }
            }
        }
        return common;
    }
}
