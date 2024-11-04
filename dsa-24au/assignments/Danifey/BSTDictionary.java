import java.util.List;

public class BSTDictionary implements Dictionary {
    List array;
    public BSTDictionary(int capacity) {
        /* NONE OF US KNOW JHAVA AND THE CLASS EXPECTS US TO KNOW JAVA - WORKED WITH TYLER, Nicole, Alexandra, and Cleo.
        int <— bstHelper(arr, target, low, high):

     if (low == high):

          if(arr[low].value == target): return low

          else return -1

 

     int mid =….

Int mid = Math.floor((high + low) / 2);

If (arr[mid].equals(target)):

Return List.of(arr[mid])

If (target < arr[mid]):

    bstHelper(arr, target, low, mid-1)

Else

      Return bstHelper(arr, target, mid+1, high)
        get array size len.Dictionary[]
        array high-low
         */

    }

    public void add(String term, String definition) {

    }

    public void remove(String term, String definition) {
    }

    public boolean checkInvariant() {
        return true;
    }

    public List<String> lookup(String term) {

        
        return List.of();

   }

    public String toString() {
        return "";
    }

}