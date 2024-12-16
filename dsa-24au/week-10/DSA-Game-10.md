# DSA Game 10 (work-in-progress)

Write your name on the quiz.
Solve three of the following nine questions to complete this game; all other questions will count as bonus.

This game is out of 15 points.

## Part I
A Thesaurus Abstract Data Type (ADT) lets you associate with an word (a string *term* ) with a collection of other distinct words with similar meanings (*synonyms*) and a collection of other distinct words with opposite meanings (*antonyms*). The order of the synonyms and antonyms doesn't matter.

Synonyms and antonyms are *symmetric*. If "concise" is a synonym of "short", then "short" should also be a synonym of "concise". They are not transitive (you don't need to propagate "concise" to also be a synonym of all of its synonyms as well, to the third degree).

Use `n` as the existing number of terms in the thesaurus. Each one is guaranteed to only have `log n` synonyms and `log n` antonyms when being added.

### Question 1 [5 points]
Write pseudocode for the following method and give its running time and space usage ($T(n)$ and $S(n)$)

```
void addTerm(String term, List<String> synonyms, List<String> antonyms)
```

### Question 2 [5 points]
Write pseudocode for the following method and give its running time and space usage ($T(n)$ and $S(n)$)

```
List<String> getSynonyms(String term)
```

### Question 3 [5 points]
Write pseudocode for the following method and give its running time and space usage ($T(n)$ and $S(n)$)

```
List<String> getAntonyms(String term)
```

## Part II

### Question 4 [5 points]

zyBooks Lab 09 - Graphs

Write next to the placeholder below your java implementation from the file AdjacencyListGraph.java, the following method.
Describe in pseudocode what it does, and give its running time and space usage in Big-Oh notation.

```java
// Returns an ArrayList of edges with the specified fromVertex.
   @Override
   public ArrayList<Edge> getEdgesFrom(Vertex fromVertex) {
      // TODO: Type your code here (remove placeholder line below)
      return new ArrayList<Edge>();
   }
```

### Question 5 [5 points]

zyBooks Lab 09 - Graphs

Write next to the placeholder below your java implementation from the file AdjacencyMatrixGraph.java, the following method
Describe in pseudocode what it does, and give its running time and space usage in Big-Oh notation.

```java
 // Adds a directed edge from the first to the second vertex. If the edge
   // already exists in the graph, no change is made and false is returned.
   // Otherwise the new edge is added and true is returned.
   @Override
   public boolean addDirectedEdge(Vertex fromVertex, Vertex toVertex) {
      // TODO: Type your code here (remove placeholder line below)
      return false;
   }
```

### Question 6 [5 points]

zyBooks Lab 10 - HashMaps

Write next to the placeholder below your java implementation from the file CourseGradebook.java, the following method
Describe in pseudocode what it does, and give its running time and space usage in Big-Oh notation.

```java
  @Override
   public ArrayList<Integer> getSortedStudentIDs() {
      // TODO: Type your code here (remove placeholder line below)
      ArrayList<Integer> results = new ArrayList<>();
      studentIds.forEach(id -> results.add(id));
      return results;
   }
```

