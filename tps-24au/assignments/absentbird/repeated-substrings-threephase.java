import java.util.Scanner;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.HashSet;

class Candidate {
  public int len;
  public Integer index1;
  public Integer index2;
  public Candidate(int l, int i1, int i2) {
    len = l;
    index1 = i1;
    index2 = i2;
  }
  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append(this.len);
    sb.append(" | ");
    sb.append(this.index1);
    sb.append(" | ");
    sb.append(this.index2);
    return sb.toString();
  }
}

class repeatedsubstrings {
  public static Map<String, HashSet<Integer>> dictionary;
  public static void main(String []args) {
    Scanner scanner = new Scanner(System.in);
    String input = scanner.nextLine();
    String lss = "";
    // Build dictionary
    String mostmatched = "";
    int matchcount = 0;
    dictionary = new HashMap<>();
    for (int i = 0; i < input.length() - 1; i++) {
      String key = input.substring(i, i+2);
      HashSet<Integer> vals = dictionary.get(key);
      if (vals == null) {
          vals = new HashSet<>();
          dictionary.put(key, vals);
      }
      vals.add(i);
      if (vals.size() > matchcount) {
        matchcount = vals.size();
        mostmatched = key;
      }
    }
    // Check most repeated string
    if (matchcount > input.length() / 26) {
      HashSet<Integer> hset = dictionary.get(mostmatched);
      Integer[] vals = hset.toArray(new Integer[hset.size()]);
      Arrays.sort(vals);
      ArrayList<Integer> sigstart = new ArrayList<>();
      int sigsize = 0;
      int signum = 0;
      int cstart = 0;
      int csize = 0;
      int cnum = 0;
      int last = 0;
      for (int i = 0; i < vals.length-1; i++) {
        int v = vals[i];
        int nv = vals[i+1];
        if (v - last == csize) {
          cnum++;
          if (cnum > signum) {
            sigstart = new ArrayList<>();
            sigstart.add(cstart);
            sigsize = csize;
            signum = cnum;
          } else if (cnum == signum && csize == sigsize) {
            sigstart.add(cstart);
          }
        } else {
          cstart = v;
          csize = nv - v;
          cnum = 1;
        }
        last = v;
      }
      if (cnum > signum) {
        sigstart = new ArrayList<>();
        sigstart.add(cstart);
        sigsize = csize;
        signum = cnum;
      } else if (cnum == signum && csize == sigsize) {
        boolean unique = true;
        for (Integer start : sigstart) {
          if (start == cstart) {
            unique = false;
            break;
          }
        }
        if (unique) {
          sigstart.add(cstart);
        }
      }
      ArrayList<Candidate> candidates = new ArrayList<>();
      if (sigstart.size() > 1) {
        for (int i = 0; i < sigstart.size(); i++) {
          for (int j = i + 1; j < sigstart.size(); j++) {
            Candidate c = new Candidate(sigsize * signum, sigstart.get(i), sigstart.get(j));
            candidates.add(c);
          }
        }
      } else {
        int start = sigstart.get(0);
        if (start + signum + sigsize > 1) {
          Candidate c = new Candidate(sigsize * signum, start, start + sigsize);
          candidates.add(c);
        }
      }
      for (Candidate c : candidates) {
        for (int i = 0; c.index1 + c.len < input.length() && c.index2 + c.len < input.length(); i++) {
          char a = input.charAt(c.index1 + c.len);
          char b = input.charAt(c.index2 + c.len);
          if (a == b) {
            c.len++;
          } else {
            break;
          }
        }
        for (int i = -1; c.index1 + i >= 0 && c.index2 + i >= 0; i--) {
          char a = input.charAt(c.index1 + i);
          char b = input.charAt(c.index2 + i);
          if (a == b) {
            c.len++;
            c.index1--;
            c.index2--;
          } else {
            break;
          }
        }
        if (lss.length() < c.len) {
          lss = input.substring(c.index1, c.index1 + c.len);
        } else if (lss.length() == c.len) {
          String str = input.substring(c.index1, c.index1 + c.len);
          if (lss.compareTo(str) > 0) {
            lss = str;
          }
        }
      }
      if (lss.length() > input.length() / 4) {
        System.out.println(lss);
        return;
      }
    }
    // Check for 4+ character strings
    HashMap<Integer, HashMap<Integer, Candidate>> candidates = new HashMap<>();
    for (HashSet<Integer> hset : dictionary.values()) {
      Integer[] vals = hset.toArray(new Integer[hset.size()]);
      for (int i = 0; i < vals.length - 1; i++) {
        int v = vals[i];
        if (v+4 > input.length()) {
          continue;
        }
        String next = input.substring(v+2, v+4);
        HashSet<Integer> nvals = dictionary.get(next);
        if (nvals == null || nvals.size() == 1) {
          continue;
        }
        for (int j = i + 1; j < vals.length; j++) {
          int nv = vals[j];
          if (nvals.contains(nv+2)) {
            Candidate c = new Candidate(4, v, nv);
            HashMap<Integer, Candidate> ch = candidates.get(v);
            if (ch == null) {
              ch = new HashMap<>();
              candidates.put(v, ch);
            }
            ch.put(nv, c);
          }
        }
      }
    }
    // Collapse candidates
    ArrayList<Candidate> finalists = new ArrayList<Candidate>();
    int longest = 0;
    for (HashMap<Integer, Candidate> ch : candidates.values()) {
      for (Candidate c : ch.values()) {
        if (c.index1 + longest > input.length() || c.index2 + longest > input.length()) {
          continue;
        }
        Map<Integer, Candidate> dh = candidates.get(c.index1 + c.len);
        while (true) {
          if (dh != null) {
            Candidate d = dh.get(c.index2 + c.len);
            if (d == null) {
              break;
            } 
            c.len += d.len;
            dh = candidates.get(c.index1 + c.len);
          } else {
            Candidate d = null;
            int i;
            int i1 = c.index1 + c.len;
            int i2 = c.index2 + c.len;
            for (i = 1; i < 4; i++) {
              dh = candidates.get(i1 - i);
              if (dh == null) {
                continue;
              }
              d = dh.get(i2 - i);
              if (d != null) {
                break;
              }
            }
            if (d == null) {
              break;
            }
            c.len += d.len - i;
            dh = candidates.get(c.index1 + c.len);
          }
          if (c.len > longest) {
            longest = c.len;
            finalists = new ArrayList<Candidate>();
            finalists.add(c);
          } else if (c.len == longest) {
            finalists.add(c);
          }
        }
        if (c.len > longest) {
          longest = c.len;
          finalists = new ArrayList<Candidate>();
          finalists.add(c);
        } else if (c.len == longest) {
          finalists.add(c);
        }
      }
    }
    // Compare finalists
    for (Candidate c : finalists) {
      for (int i = 0; c.index1 + c.len < input.length() && c.index2 + c.len < input.length(); i++) {
        char a = input.charAt(c.index1 + c.len);
        char b = input.charAt(c.index2 + c.len);
        if (a == b) {
          c.len++;
        } else {
          break;
        }
      }
      for (int i = 1; c.index1 - i >= 0 && c.index2 - i >= 0; i++) {
        char a = input.charAt(c.index1 - i);
        char b = input.charAt(c.index2 - i);
        if (a == b) {
          c.len++;
          c.index1--;
          c.index2--;
        } else {
          break;
        }
      }
      if (c.len < lss.length()) {
        continue;
      }
      String str = input.substring(c.index1, c.index1 + c.len);
      if (str.length() == lss.length() && lss.compareTo(str) < 0) {
        continue;
      }
      lss = str;
    }
    if (lss.length() > 0) {
      System.out.println(lss);
      return;
    }
    // Check for two or three character substring
    for (HashSet<Integer> hset : dictionary.values()) {
      if (hset.size() < 2) {
        continue;
      }
      char third = '\u0000';
      Integer[] vals = hset.toArray(new Integer[hset.size()]);
      for (int i = 0; i < vals.length - 1; i++) {
        int i1 = vals[i];
        if (i1 + 3 > input.length()) {
          continue;
        }
        char nc = input.charAt(i1 + 2);
        for (int j = i + 1; j < vals.length; j++) {
          int i2 = vals[j];
          if (i2 + 3 > input.length()) {
            continue;
          }
          if (input.charAt(i2 + 2) == nc) {
            if (third == '\u0000' || nc < third) {
              third = nc;
            }
          }
        }
      }
      String str = input.substring(vals[0], vals[0]+2) + third;
      if (str.length() > lss.length() || (str.length() == lss.length() && lss.compareTo(str) > 0)) {
        lss = str;
      }
    }
    if (lss.length() > 0) {
      System.out.println(lss);
      return;
    }
    // Check for single repeating character
    HashSet<Character> alphabet = new HashSet<>();
    for (int i = 0; i < input.length(); i++) {
      char c = input.charAt(i);
      if (alphabet.contains(c)) {
        if (c == 'a') {
          System.out.println(c);
          return;
        }
        String str = String.valueOf(c);
        if (lss.length() == 0 || lss.compareTo(str) > 0) {
          lss = str;
        }
      } else {
        alphabet.add(c);
      }
    }
    System.out.println(lss);
    return;
  }
}
