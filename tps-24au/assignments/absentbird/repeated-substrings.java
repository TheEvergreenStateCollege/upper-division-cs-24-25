import java.util.Collection;
import java.util.Scanner;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

class repeatedsubstrings {
  public static Map<String, Set<Integer>> dictionary;
  public static void main(String []args) {
    Scanner scanner = new Scanner(System.in);
    String input = scanner.nextLine();
    String lss = "";
    dictionary = new HashMap<>();
    for (int i = 0; i < input.length(); i++) {
      String key = input.substring(i, i+1);
      HashSet<Integer> vals = dictionary.get(key);
      if (vals == null) {
          vals = new HashSet<Integer>();
          dictionary.put(key, vals);
      }
      vals.add(i);
    } 
    int[] nextlen = new int[input.length()];
    int currentlen = input.length() - 1;
    while (currentlen > 1) {
      for (int i = 0; i < input.length(); i++) {
        if (i + currentlen > input.length()-1) {
          break;
        }
        if (nextlen[i] < 0 || (nextlen[i] > 0 && nextlen[i] < currentlen)) {
          continue;
        }
        String key = input.substring(i, i+1);
        HashSet<Integer> vals = dictionary.get(key);
        int vi = vals.indexOf(i);
        if (vi == vals.size() - 1) {
          nextlen[i] = -1;
          continue;
        }
        for (int j = vi + 1; j < vals.size(); j++) {
          int nextc = vals.get(j);
          int nexte = nextc + currentlen;
          if (nextc + currentlen > input.length()) {
            nextlen[i] = nexte + (input.length() - nexte);
            continue;
          }
          String current = input.substring(i, i + currentlen);
          String candidate = input.substring(nextc, nexte);
          if (candidate.equals(current)) {
            if (current.length() > lss.length()) {
              lss = current;
            } else if (current.length() == lss.length() && lss.compareTo(current) > 0) {
              lss = current;
            }
          }
        }
      }
      if (lss.length() > 0) {
        System.out.println(lss);
        return;
      }
      currentlen--;
    }
    Map<Character, Integer> alphabet = new HashMap<>();
    for (int i = 0; i < input.length(); i++) {
      char c = input.charAt(i);
      int count = alphabet.get(c);
      if (count == 1) {
        if (c == 'a') {
          System.out.println(c);
          return;
        }
        String str = String.valueOf(c);
        if (lss.length() == 0 || lss.compareTo(str) > 0) {
          lss = str;
        }
      } else if (count < 2) {
        alphabet.put(c, count+1);
      }
    }
    if (lss.length() > 0) {
      System.out.println(lss);
      return;
    }
  }
}
