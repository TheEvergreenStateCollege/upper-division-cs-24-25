import java.util.List;
import java.util.ArrayList;

public class BSTDictionary implements Dictionary {
<<<<<<< HEAD
    List array;
    public BSTDictionary(int capacity) {
        this.array=
=======

    List array;

    public BSTDictionary(int capacity) {
        this.array = new ArrayList<>(capacity);
>>>>>>> 5fffd0a8ae5614f2f8b490aad75f84d3f5e25cab
    }

    public void add(String term, String definition) {

    }

    public void remove(String term, String definition) {
    }

    public boolean checkInvariant() {
        return true;
    }

    public List<String> lookup(String term) {
        Dictionary d;
        int low = 0;
        int high - d.length -1;
        int mid = low + (low + high)/2;
        
        char firsT = term.charAt(0);

      // exlist = [0, 1, 2, 3, 4]
      // key = 4;
        

        if(high == low){
            return List[low];
        }
        if(d[mid] == term){
            return term;
        }
        else{
            if(firsT > d[mid].charAt(0)){

            }
            else if(firsT < d[mid].charAt(0)){

            }
            else if(firsT == d[mid].charAt(0)){


            }



        }
        return list.of();

   }

    public String toString() {
        return "";
    }

}