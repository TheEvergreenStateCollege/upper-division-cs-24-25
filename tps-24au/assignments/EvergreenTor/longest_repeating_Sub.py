
def LongestRepeatingSubstring(string):

    if string == "":
        return 0

    best_so_far = ""
    repeating_substrings = []

    for i in range(len(string)):
        for j in range(i+1,len(string) + 1):
            substring = string[i:j] 
            #repeating_substrings += (j,substring)
            repeating_substrings.append(substring) 
    #return repeating_substrings
    
    for i in range(len(repeating_substrings)):
        for j in range(i+1, len(repeating_substrings)):
            if repeating_substrings[i] == repeating_substrings[j]:
                if len(repeating_substrings[i]) > len(best_so_far):
                    best_so_far = repeating_substrings[i]
            
    return best_so_far

        
print(LongestRepeatingSubstring("aabcabc"))   
    
#return longest substring that occurs consecutivley at least twice, could be empty string.
# Example: "aabcabc" -> "abc" 
#Example 2, "banana" -> "na" or "an"

