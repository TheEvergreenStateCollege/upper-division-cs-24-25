class Node:
    def __init__(self,parent):
        self.parent = parent
        self.children = {}

    def addNode(self,letter):
        new_node = Node(self)
        self.children[letter] = new_node
    
    def getChild(self, char):
        return Node(self.children.get(char))

    def insertChild(self, suffix):
         
        if len(suffix) == 0:
            return False 
        
        c = suffix[0]
        inserted = False

        # n is either existing child for character c or a new child

        n = Node

        if c in self.children:
            n = self.children[c]
        else:
            n = Node(self)
            self.children[c] = n
            
            inserted = n.insertChild(suffix[1:])
        return inserted 
        
class PrefixTree:
    def __init__(self):
        self.root = Node(None)

    def lookUP(self,string):
        curr = Node(self.root)
        for i in range(len(string)):
            curr = curr.getChild(string[i])
            if curr is None:
                return i 
        
        return len(string)
    
    def insert(self, string):
        return self.root.insertChild(string)
    
    def toString(self):
        return "PrefixTree: " + self.root.str()
    

    


        

        






        
    
    

    