import java.util.List;
import java.util.ArrayList;

public class BSTDictionary implements Dictionary {

    List array;

    public BSTDictionary(int capacity) {
        this.array = new ArrayList<>(capacity);
    }

    public void add(String term, String definition) {
    }

    public void remove(String term, String definition) {
    }

    public boolean checkInvariant() {
        return true;
    }

    public List<String> lookup(String term) {

        // TODO replace this
        return List.of();

   }

    public String toString() {
        return "";
    }

}