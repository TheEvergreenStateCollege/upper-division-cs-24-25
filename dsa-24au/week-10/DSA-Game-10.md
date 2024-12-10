# DSA Game 10 (work-in-progress)

Write your name on the quiz.
Solve three of the following nine questions to complete this game; all other questions will count as bonus.
## Part I
A Thesaurus Abstract Data Type (ADT) lets you associate with an word (a string *term* ) with a collection of other distinct words with similar meanings (*synonyms*) and a collection of other distinct words with opposite meanings (*antonyms*). The order of the synonyms and antonyms doesn't matter.

Synonyms and antonyms are *symmetric*. If "concise" is a synonym of "short", then "short" should also be a synonym of "concise". They are not transitive (you don't need to propagate "concise" to also be a synonym of all of its synonyms as well, to the third degree).

Use `n` as the existing number of terms in the thesaurus. Each one is guaranteed to only have `log n` synonyms and `log n` antonyms when being added.

### Question 1
Write pseudocode for

```
void addTerm(String term, List<String> synonyms, List<String> antonyms)
```
