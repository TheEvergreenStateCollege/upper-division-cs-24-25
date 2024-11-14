class Node:
    def __init__(self,parent):
        self.parent = parent
        self.children = {}

    def addNode(self,letter):
        new_node = Node(self)
        self.children[letter] = new_node

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

    


        

        






        
    
    

    