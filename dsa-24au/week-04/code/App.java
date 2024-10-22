import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class App {
    final static Path PATH = Paths.get("../data/pg29765.txt");

    private static Dictionary loadDictionary() {
        long start = System.currentTimeMillis();
        Dictionary result = loadDictionaryHelper();
        long elapsed = System.currentTimeMillis() - start;
        System.out.println(String.format("Dictionary load time {}", Long.toString(elapsed)));
        return result;
    }

    private static Dictionary loadDictionaryHelper() {
        Charset charset = StandardCharsets.UTF_8;

        Dictionary d = new LinearDictionary();

        try {
            List<String> lines = Files.readAllLines(PATH, charset);
            int start = 0;
            boolean defMode = false;
            String term = null;
            StringBuilder defn = null;
            for (int i = 0; i < lines.size(); i += 1) {
                if (defMode) {
                    if (lines.get(i).isBlank()) {
                        defMode = false;
                        if (term != null) {
                            d.add(term, defn.toString());
                            System.out.println(term);
                            System.out.println(i);
                            term = null;
                            defn = null;
                        }
                    } else {
                        defn.append(lines.get(i));
                    }
                } else if (lines.get(i).startsWith("Defn")) {
                    defMode = true;
                    // The term when we find one that begins with "defn" is three lines above
                    term = lines.get(i-3);
                    defn = new StringBuilder();
                }
            }
        } catch (IOException ex) {
            System.out.format("I/O error: %s%n", ex);
        }
        return d;
    }
    
    public static void main(String[] args) {

        if (args.length < 1) {
            System.err.println("Usage: java Dictionary <searchterm>");
        }
        String searchTerm = args[0];

        Dictionary d = loadDictionary();        

        long start2 = System.currentTimeMillis();
        List<String> found = d.lookup(searchTerm);
        long elapsed2 = System.currentTimeMillis() - start2;
        System.out.println(String.format("Dictionary load time {}", Long.toString(elapsed2)));

        System.out.println(String.format("Definitions of {}", searchTerm));
        System.out.println(found);
    }

}