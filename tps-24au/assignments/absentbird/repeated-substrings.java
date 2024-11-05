import java.util.Collection;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.HashMap;
import java.util.Map;

class repeatedsubstrings {
  public static Map<Character, ArrayList<Integer>> dictionary;
  public static void main(String []args) {
    Scanner scanner = new Scanner(System.in);
    String input = scanner.nextLine();
    String lss = "";
    dictionary = new HashMap<>();
    for (int i = 0; i < input.length(); i++) {
      char c = input.charAt(i);
      ArrayList<Integer> vals = dictionary.get(c);
      if (vals == null) {
          vals = new ArrayList<Integer>();
          dictionary.put(c, vals);
      }
      vals.add(i);
    } 
    int currentlen = input.length() - 1;
    while (currentlen > 1) {
      for (int i = 0; i < input.length(); i++) {
        if (i + currentlen > input.length()-1) {
          break;
        }
        char c = input.charAt(i);
        ArrayList<Integer> vals = dictionary.get(c);
        int vi = vals.indexOf(i);
        if (vi == vals.size() - 1) {
          continue;
        }
        for (int j = vi + 1; j < vals.size(); j++) {
          int nextc = vals.get(j);
          if (nextc + currentlen > input.length()) {
            continue;
          }
          String current = input.substring(i, i + currentlen);
          String candidate = input.substring(nextc, nextc + currentlen);
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
    for (char c = 'a'; c <= 'z'; c++) {
      ArrayList<Integer> vals = dictionary.get(c);
      if (vals.size() > 1) {
        System.out.println(c);
        return;
      }
    }
  }
}
