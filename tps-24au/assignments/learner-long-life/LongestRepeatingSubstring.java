import java.util.*;

public class LongestRepeatingSubstring {

    public static String longestRepeatingSubstring(String s) {
        int n = s.length();
        if (n == 0) return "";

        // Step 1: Build suffix array
        int[] suffixArray = buildSuffixArray(s);
        
        // Step 2: Build LCP array
        int[] lcp = buildLCP(s, suffixArray);
        
        // Step 3: Find the maximum LCP and its corresponding substring
        int maxLCP = 0;  // Track the maximum LCP value
        int index = -1;  // Track the suffix array index corresponding to maxLCP

        for (int i = 1; i < lcp.length; i++) {
            if (lcp[i] > maxLCP) {
                maxLCP = lcp[i];
                index = i;
            } else if (lcp[i] == maxLCP) {
                // Resolve ties lexicographically
                String current = s.substring(suffixArray[i], suffixArray[i] + lcp[i]);
                String best = s.substring(suffixArray[index], suffixArray[index] + lcp[index]);
                if (current.compareTo(best) < 0) {
                    index = i;
                }
            }
        }

        // If no repeated substring is found, return empty string
        if (maxLCP == 0) return "";

        // Extract and return the longest repeated substring
        return s.substring(suffixArray[index], suffixArray[index] + maxLCP);
    }

    // Function to build the suffix array of a string
    private static int[] buildSuffixArray(String s) {
        int n = s.length();
        Integer[] suffixes = new Integer[n];
        for (int i = 0; i < n; i++) {
            suffixes[i] = i;
        }

        Arrays.sort(suffixes, (a, b) -> s.substring(a).compareTo(s.substring(b)));

        int[] suffixArray = new int[n];
        for (int i = 0; i < n; i++) {
            suffixArray[i] = suffixes[i];
        }
        return suffixArray;
    }

    // Function to build the LCP (Longest Common Prefix) array
    private static int[] buildLCP(String s, int[] suffixArray) {
        int n = s.length();
        int[] rank = new int[n];
        int[] lcp = new int[n - 1];

        // Build rank array: rank[i] is the rank of the suffix starting at index i
        for (int i = 0; i < n; i++) {
            rank[suffixArray[i]] = i;
        }

        int h = 0;
        for (int i = 0; i < n; i++) {
            if (rank[i] > 0) {
                int j = suffixArray[rank[i] - 1];
                while (i + h < n && j + h < n && s.charAt(i + h) == s.charAt(j + h)) {
                    h++;
                }
                lcp[rank[i] - 1] = h;
                if (h > 0) {
                    h--;
                }
            }
        }
        return lcp;
    }

    public static void main(String[] args) {
        // Read input string from command-line arguments
        if (args.length == 0) {
            System.out.println("Error: Please provide an input string.");
            return;
        }

        String s = args[0];
        String result = longestRepeatingSubstring(s);
        System.out.println(result); // Output the longest repeating substring
    }
}
