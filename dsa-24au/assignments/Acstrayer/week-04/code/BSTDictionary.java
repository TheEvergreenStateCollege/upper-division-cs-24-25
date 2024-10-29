import java.util.List;
import java.util.ArrayList;

public class BSTDictionary implements Dictionary {

    List<String> terms;
    List<String> definitions;

    public BSTDictionary() {
        this.terms = new ArrayList<>();
        this.definitions = new ArrayList<>();
    }

    public void add(String term, String definition) {
        if (term == null || term.isBlank()) {
            return;
        }

        List<String> definitions = lookup(term);

        if (definitions.contains(definition)) {
            // We already contain this definition for this term
            return;
        }

        // This is a new term-definition association, add it to our lists.
        this.terms.add(term);
        this.definitions.add(definition);
    }

    public void remove(String term, String definition) {
        if (term == null || term.isBlank()) {
            return;
        }

        List<String> definitions = lookup(term);

        int index = definitions.indexOf(definition);

        // index could be -1 which means not found
        // we ignore that case
        if (index >= 0 && index < definitions.size()) {
            // If definition was found, remove the term at the associated position,
            // so that terms and definitions list match
            terms.remove(index);
        }

    }

    public boolean checkInvariant() {
        return this.terms.size() == this.definitions.size();
    }

    public List<String> lookup(String term) {

        if (term == null || term.isBlank()) {
            // return empty list
            return List.of();
        }


        List<String> result = new ArrayList<>();

        int low = 0;
        int high = this.terms.size() - 1;

        while (high >= low) {
            int mid = low + (high - low) / 2;

            if (this.terms.get(mid).equals(term)) {
                System.out.println("SUCCESS!!" + terms.get(mid));
                result.add(definitions.get(mid));
            } else if (this.terms.get(mid).compareTo(term) < 0) {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

       
        return result;

    }

    public String toString() {
        return String.format("BST dictionary with {} term-definition pairs.", Integer.toString(this.terms.size()));
    }
}