public class longestRepeatingSubstring{


    class Candidate {

        int startIndex; // where this candidate starts in original string
        int endIndex;   // where this candidate ends in original string
        String original;

        public Candidate(String original) {
            this.original = original;

    
        }
        public Candidate(String original, int startIndex, int endIndex) {
            this.original = original;
            this.startIndex = startIndex;
            this.endIndex = endIndex;
        }

        public String Candidate getCandidate() {
            return original;
        }

        public int getStartIndex() {
         return startIndex;
        }
        
        public int getEndIndex() {
            return endIndex;
        }
    
    }
    

    public static String longestRepeatingSubstring(String str) {
        if (str == null || str.length() < 2)
        return "";
         
        String candidate= new Candidate(s);

        List<Candidate> substringsList = new ArrayList<Candidate>();

        //Goes through and finds all the substrings
        for(int j = str.length(); j >= 0; j--){
            for(int i = 0; i < str.length(); i++){
                String substring = str.substring(i,j);
                substringsList.add(new Candidate(s,i,j));
            }
        }

        String bestSoFar = "";
        //Compares the substring to find the longest repeating substring
        for(int i = 0; i < substringsList.length(); i++) {
            for(int j = i + 1; j < substringList.length(); j++) {
                if(substringList<i>.getCandidate().equals(substringList<j>.getCandidate())) {
                    if(substringList<i>.getStartIndex() != substringList<j>.getStartIndex() && substringList<i>.getEndIndex() != substringList<j>.getEndIndex()) {
                        bestSoFar = substringList<i>.getCandidate();
                    }
                } 
            }
        }
        return bestSoFar;

    }
}


    public static void main(String[] args) {
        String result = longestRepeatingSubstring("aabcabc");
        System.out.println(result);  // Output: abc
        assert(result.equals("abc"));
    }