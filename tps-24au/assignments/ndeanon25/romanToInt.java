import java.util.HashMap;
import java.util.Map;

class Solution {
    public int romanToInt(String s) {
      Map<String,Integer> romanToInt= new HashMap<>(); 
       
       romanToInt.put("I", 1);
       romanToInt.put("V", 5);
       romanToInt.put("X", 10);
       romanToInt.put("L", 50);
       romanToInt.put("C", 100);
       romanToInt.put("D",500);
       romanToInt.put("M",1000);
       s = s.replace("IV", "IIII");
       s = s.replace("IX", "VIII");
       s = s.replace("XL", "XXXX");
       s = s.replace("XC", "LIIII");
       s = s.replace("CD", "CCCC");
       s = s.replace("CM", "DCCCC");

       int result = 0;
       for ( int i = 0; i < s.length(); i++) {
         if (i+1 < s.length() && romanToInt.get(s.substring(i, i+2))!= null) {
             result += romanToInt.get(s.substring(i, i+2));
             i++;
         } else {
             result += romanToInt.get(s.substring(i, i+1));
         }
       }
    return result;
    }  
}
