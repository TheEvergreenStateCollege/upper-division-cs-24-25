import java.util.ArrayList;

class LongestRepeatingSubstring {
public static void main(String[] args) {
        String sample = "abcdabc";

        ArrayList<String> substrings = new ArrayList<>();

        //generate substrings:
        //pointers in java?
        int left = 0;

        //first case -- first character to 1 from last
        for (int right = 1; right < sample.length() - 1; ++right) {
            substrings.add(sample.substring(left, right + 1));
            //System.out.println(substrings.get(right - 1));
        }
        
        //
        for (left = 1; left < sample.length() - 1; ++left) {
            
            for(int right = left + 1; right < sample.length(); ++right) {
                
                if (left != right) {
                    substrings.add(sample.substring(left, right));
                    //System.out.println(left + ", " + right);
                }

            }
        
        }


        //compare substrings for matches
        //loop through substrings 
        int longestLength = 0;
        String longestSubstring = "";
        
        for (int i = 0; i < substrings.size(); ++i) {
            
            for (int j = 0; j < substrings.size(); ++j) {
                if (j != i) {
                    if (substrings.get(i) == substrings.get(j)) {
                        if (substrings.get(i).length() > longestLength) {
                            longestSubstring = substrings.get(i);
                        }
                    }
                }
            }

        }
        

    }

}