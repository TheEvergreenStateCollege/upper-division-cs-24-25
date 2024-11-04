import java.util.Scanner;
import java.util.HashMap;
import java.util.Map;

class repeatedsubstrings {
    public static void main(String []args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();
        String lss = "";
        Map<String, Integer> dictionary = new HashMap<>();
        for (int i = 0; i < input.length(); i++) {
            char l = input.charAt(i);
            String str = String.valueOf(l); 
            if (dictionary.get(str) != null) {
                dictionary.put(str, 2);
                if (str.length() > lss.length()) {
                    lss = str;
                }
            } else {
                dictionary.put(str, 1);
            }
            if (i < 1) {
                continue;
            }
            for (int j = i-1; j >= 0; j--) {
                char k = input.charAt(j);
                str = k + str;
                if (dictionary.get(str) != null) {
                    dictionary.put(str, 2);
                    if (str.length() > lss.length()) {
                        lss = str;
                    }
                } else {
                    dictionary.put(str, 1);
                }
            }
        }
        System.out.println(lss);
    }
}
