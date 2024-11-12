class Node:
    def __init__(self,parent):
        self.parent = parent
        self.children = {}

    def addNode(self,letter):
        new_node = Node(self)
        self.children[letter] = new_node
        
class PrefixTree:
    def __init__(self):
        self.root = Node(None)
        
    
    

    