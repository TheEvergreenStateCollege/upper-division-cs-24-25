
def LongestRepeatingSubstring(string):

    if string == "":
        return 0

    repeating_substrings = []

    for i in range(len(string)):
        for j in range(i+1,len(string) + 1):
            substring = string[i:j + 1] 
            repeating_substrings += (j,substring) 
    return repeating_substrings
    
    #
        
            

print(LongestRepeatingSubstring("banana"))   
    

    
        
        

        #return longest substring that occurs consecutivley at least twice, could be empty string.
        # Example: "aabcabc" -> "abc" 
        #Example 2, "banana" -> "na" or "an"




