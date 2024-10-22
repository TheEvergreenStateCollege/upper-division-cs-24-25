import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.Optional;

/**
 * An Abstract Data Type representing a dictionary,
 * an association of terms and their definitions,
 * allowing addition and removal of this association, and lookup
 * of definitions by the term.
 * 
 * Currently it only works on string terms and string definitions.
 */
public interface Dictionary {

    /**
     * Add the given pair of dictionary term and definition to this dictionary.
     * May be in addition to other, distinct definitions for the same term.
     * If this is the same definition for the same term as already exists in the dictionary, this method has no effect.
     * @param term - the String of the term to lookup (if empty or null, this method has no effect)
     * @param definition - the String of the definition for the given term (may be empty or null)
     */
    public void add(String term, String definition);

    /**
     * Remove the given pair of dictionary term and definition to this dictionary.
     * Should not change other definitions for the same term in dictionary if they exist.
     * @param term - the String of the term whose association to remove (if empty or null, this method has no effect)
     * @param definition - the String of the definition whose association with the given term to remove (may be empty or null)
     */
    public void remove(String term, String definition);

    /**
     * Lookup and return a list of definitions associated with the given term.
     * List may be empty or contain only a single item, or multiple, but null will not be returned.
     * @param term - the String of the term to lookup associations
     */
   public List<String> lookup(String term);

}
