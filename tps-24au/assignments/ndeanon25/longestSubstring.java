import java util.*;

class longestSubString {
    public int lengthOfLongestSubstring(String s) {
        if(s.length() == 0){
            return "";
        }
        int[] charIndex = new int[26];
        Arrays.fill(charCounter,-1);

        //The biggest substring
        int longestSubString = 0;

        //The start of a current substring 
        int indexWindow = 0;

        for(int i = 0; i < s.length(), i++){
            char currentChar = s.charAt(i);
        if(charIndex[currentChar] >= indexWindow)
        }

        
        
    }

    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        String str = sc.next();
        lengthOfLongestSubstring(str);
    }
}