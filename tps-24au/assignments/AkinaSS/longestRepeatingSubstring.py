def longestRepeatingSubstring(s):
    if s == "":
        return ""
    
    best_so_far = ""
    
    repeatingsubtring = []
    for i in range(len(s)):
        for j in range(i+1, len(s)+1):
            substring = s[i:j]
            repeatingsubtring.append(substring)
            #print(i, j, substring)
    #print(len(repeatingsubtring))
            
    for i in range(len(repeatingsubtring)):
        for j in range(i+1, len(repeatingsubtring)):
            if repeatingsubtring[i] == repeatingsubtring[j]:
                if len(repeatingsubtring[i]) > len(best_so_far):
                    best_so_far = repeatingsubtring[i]
            
    return best_so_far

def main():
    stringVal = input("Enter the string: ")
    print(longestRepeatingSubstring(stringVal))


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
