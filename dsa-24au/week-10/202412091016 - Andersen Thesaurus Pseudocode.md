---
tags:
---

# Pseudocode for Thesaurus
```pseudocode
struct thesaurusEntry
    String term
    list<String> synonyms
    list<String> antonyms

class Thesaurus {

// one hashmap with two nested lists in the value
   Map<String, ThesaurusEntry> entries;

// alternative with two parallel hashmaps
   Map<String, List<String> synonyms;
   Map<String, List<String> antonyms;   

// you can also keep parallel graphs
   Graph<String,String> synonyms;
   Graph<String,String> antonyms;

}

list<String> getSynonyms(String term)
    int hash = hashFunc(term)
    if hashFetch(hash) = null
        return []
    else 
        return hashFetch(hash).synonyms

list<String getAntonyms(String term)
    int hash = hashFunc(term)
    if hashFetch(hash) = null
        return []
    else 
        return hashFetch(hash).antonyms

void addTerm(String term, list<String> initSynonyms, list<String> initAntonyms)
    int hash = hashFunc(term)
    newEntry = new thesaurusEntry
    newEntry.term = term
    newEntry.synonyms = initSynonyms
    newEntry.antonyms = initAntonyms
    
    for string i in synonyms
        if hashFetch(hashfunc(i)).synonyms.contains(term)
            cont
        else
            hashFetch(hashfunc(i)).synonyms.append(term)
    
    for string i in antonyms
        if hashFetch(hashfunc(i)).antonyms.contains(term)
            cont
        else
            hashFetch(hashfunc(i)).antonyms.append(term)
    
    hashArray[hash] = newEntry
    
    return
```


# References
- 