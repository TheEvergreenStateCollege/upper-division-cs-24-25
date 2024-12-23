import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        PrefixTree pt = new PrefixTree();
        Scanner sc = new Scanner(System.in);
        String input = "";
        while (sc.hasNextLine()) {
            input = sc.next();
        }
        // String input = "banana";

        for (int i = 0; i < input.length(); i++) {
            pt.lookupAndInsert(input.substring(i));
        }

        String result = pt.findLongestRepeatingSubstring();
        System.out.println("Longest Repeating Substring: " + result);

        // pt.lookupAndInsert("banana");
        // int result = pt.lookup("banana");
        // assert(result == 6);
        // int result2 = pt.lookup("banan");
        // assert(result2 == 5);
        // System.out.println(pt);
        // boolean insertSuccess;
        // String  longestSoFar = "";

        // for (int i = 0; i < input.length(); i += 1) {
        //     for (int j = i + longestSoFar.length() + 1; j < input.length(); j += 1) {
        //         String slice = input.substring(i, j);
        //         insertSuccess = pt.lookupAndInsert(slice); 
        //         if ((!insertSuccess) && (slice.length() > longestSoFar.length())) {
        //             longestSoFar = slice;
        //         }
        //     }
        //     // Invariant: longestSoFar contains the LRS of all substring 
        //     // begin with character i or before
        // }
        // System.out.println(longestSoFar);
        // Invariant: longestSoFar contains the LRS of all remaining string
        
        // Example string, add all suffixes
        
        // Find the longest repeated substring
    }
}
