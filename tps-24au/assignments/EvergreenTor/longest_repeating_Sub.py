
def LongestRepeatingSubstring(s):
    if s == "":
        return 0
    best_so_far = ""
    
    for c in s:
        c += best_so_far
    return best_so_far
    
    
print(LongestRepeatingSubstring("Banana"))
    
        
        

        #return longest substring that occurs consecutivley at least twice, could be empty string.
        # Example: "aabcabc" -> "abc" 
        #Example 2, "banana" -> "na" or "an"




