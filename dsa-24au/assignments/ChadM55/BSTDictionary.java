import java.util.List;
import java.util.ArrayList;

public class BSTDictionary implements Dictionary {

    List array;

    public BSTDictionary() {
        //this.array = new ArrayList<>; //might need to add capacity to ArrayList
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
        int low = 0;
        int high = array.length - 1;
        int mid = low + (high - low)/2;

        exList = [0, 1, 2, 3, 4]
        key = 4

        if (high == low) {
            return List[low];
        }
        return List.of();

   }

    public String toString() {
        return "";
    }

}