
class Suffix_tree:
    def __init__(self,input_string):
        self.input_string = input_string + "$" # Append the unique terminator
        self.root_node = Node(None,None) 
    
    def addSuffix():
        pass

    def searchForSubstrings():
        pass

class Node:
    def __init__(self,parent,suffix_link):
        self.parent = parent
        self.children = {}
        self.suffix_link = suffix_link # Suffix link (for Ukkonen's algorithm)




