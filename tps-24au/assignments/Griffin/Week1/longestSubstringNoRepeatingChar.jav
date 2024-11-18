import java.util.HashMap;

class Solution {
    int maxLength = 0;
    ArrayList<String> subStrings = new ArrayList<String>();
    int leftIndex = 0;
    int rightIndex = 1;
    String tempString = "";

    ArrayList<String> getSubstrings(String s) {
        ArrayList<String> subStrings = new ArrayList<String>();
        HashMap<Character, Boolean> substringChars = new HashMap<>();

        while(rightIndex < s.length()) {
            //left and right are equal
            if (s.charAt(leftIndex) == s.charAt(rightIndex)) {
                //add substring to substrings
                subStrings.add(s.substring(leftIndex, rightIndex));

                //remove left value from hashmap
                substringChars.remove(s.charAt(leftIndex));

                //move left index
                leftIndex += 1;

                //prevent overlap
                if (leftIndex == rightIndex) {
                    rightIndex += 1;
                }

            }

            //if value at right index is already in hashmap
            else if (substringChars.containsKey(s.charAt(rightIndex))) {
                //add substring to substrings
                subStrings.add(s.substring(leftIndex, rightIndex));

                //clear hash?
                substringChars.clear();

                //move left to right
                leftIndex = rightIndex;

                //prevent overlap
                rightIndex += 1;
            } 

            else {
                substringChars.put(s.charAt(rightIndex), true);
                rightIndex += 1;
            }            
        }
        return subStrings;
    }

    public int lengthOfLongestSubstring(String s) {
        //case: empty string
        if (s == "") {
            //System.out.println("Maxlength = 0");
            return maxLength;
        }
        
        //create substrings with sliding window
        subStrings = getSubstrings(s);
        
        //loop through array. If substring is longer than maxLength, then maxLen = substring.length()
        for (int i = 0; i < subStrings.size(); ++i) {
            //System.out.println("here");
            if(subStrings.get(i).length() > maxLength) {
                maxLength = subStrings.get(i).length();
                //System.out.println("new longest substring is: " + subStrings.get(i));
            }
        }

        return maxLength;
    }
}