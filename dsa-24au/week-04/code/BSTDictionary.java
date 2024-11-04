import java.util.List;
import java.util.ArrayList;

public class BSTDictionary implements Dictionary {
<<<<<<< HEAD
    List array;
    public BSTDictionary(int capacity) {
        this.array=
=======

<<<<<<< HEAD
    public BSTDictionary() {
        //this.array
=======
    List array;

<<<<<<< HEAD
    public BSTDictionary() {
        //this.array = new ArrayList<>; //might need to add capacity to ArrayList
=======
    public BSTDictionary(int capacity) {
        this.array = new ArrayList<>(capacity);
>>>>>>> 5fffd0a8ae5614f2f8b490aad75f84d3f5e25cab
>>>>>>> 349d2abae5e57afe8c94487d465bf2be7bd189a9
>>>>>>> 74305d13dc452b53a66c8a9117aa9182506249e5
    }

    public void add(String term, String definition) {

    }

    public void remove(String term, String definition) {
    }

    public boolean checkInvariant() {
        return true;
    }

    public List<String> lookup(String term) {

<<<<<<< HEAD
        // TODO replace this

=======
        
>>>>>>> 74305d13dc452b53a66c8a9117aa9182506249e5
        return List.of();

   }

    public String toString() {
        return "";
    }

}