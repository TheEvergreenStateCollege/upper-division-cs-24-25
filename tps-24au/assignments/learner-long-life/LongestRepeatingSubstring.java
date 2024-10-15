public class LongestRepeatingSubstring {

    class Candidate {

        int startIndex; // where this candidate starts in original string
        int endIndex;   // where this candidate ends in original string
        String original;
        int current;

        public Candidate(String original, int startIndex, int endIndex) {
            this.original = original;
            this.startIndex = startIndex;
            this.endIndex = endIndex;
            this.current = 0;
        }

        // Match the current character
        public boolean match(String singleChar) {

        }
    }

    public static String longestRepeatingSubstring(String s) {
        // By default, return empty substring,
        // need to improve this

        String candidate = new Candidate();

        for (int i = 0; i < s.length(); s += 1) {
            String current = s.substring(i,i+1);
            if (candidate.equals("")) {
                // if empty candidate, any current character is our best answer so far
                candidate = new Candidate(s, i, i+1);
            } else if (current.equals(candidate.substring(i,i+1)) {
                // current character matches first of our candidate,
                // we could be starting again
            }
            if (s.substring(i,i+1) 
        }
        return "";
    }

    public static void main(String[] args) {
        String result = longestRepeatingSubstring("aabcabc");
        assert(result.equals("abc"));
    }
}