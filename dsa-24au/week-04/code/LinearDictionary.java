import java.util.List;
import java.util.ArrayList;

public class LinearDictionary implements Dictionary {

    List<String> terms;
    List<String> definitions;

    public LinearDictionary() {
        this.terms = new ArrayList<>();
        this.definitions = new ArrayList<>();
    }

    public void add(String term, String definition) {
        assert(this.checkInvariant());
        if (term == null || term.isBlank()) {
            return;
        }

<<<<<<< HEAD
        /*List<String> definitions = lookup(term);
=======
        // List<String> definitions = lookup(term);
>>>>>>> 349d2abae5e57afe8c94487d465bf2be7bd189a9

        // if (definitions.contains(definition)) {
            // We already contain this definition for this term
<<<<<<< HEAD
            return;
        }*/
=======
        //    return;
        // }
>>>>>>> 349d2abae5e57afe8c94487d465bf2be7bd189a9

        // This is a new term-definition association, add it to our lists.
        this.terms.add(term);
        this.definitions.add(definition);
<<<<<<< HEAD
=======
        assert(this.checkInvariant());
>>>>>>> 349d2abae5e57afe8c94487d465bf2be7bd189a9
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

        for (int i = 0; i < this.terms.size(); i += 1) {
            System.out.println(terms.get(i));
            if (terms.get(i) == term) {
                result.add(definitions.get(i));
            }
        }

        return result;

    }

    public String toString() {
        return String.format("Linear dictionary with {} term-definition pairs.", Integer.toString(this.terms.size()));
    }
}