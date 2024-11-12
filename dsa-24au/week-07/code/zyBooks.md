 5.8 LAB: Grocery list editor with undo stack
lab activity
5.8.1: LAB: Grocery list editor with undo stack
0 / 10

In this lab a grocery list editor with undo functionality is implemented.
Step 1: Inspect the UndoCommand abstract base class

The read-only UndoCommand.java file declares the UndoCommand abstract base class. The UndoCommand class represents a command object: an object that stores all needed information to execute an action at a later point in time. For this lab, a command object stores information to undo a grocery list change made by the user.

Step 2: Inspect the incomplete GroceryList class

The GroceryList class is declared in GroceryList.java. Two fields are declared:

    listItems: An ArrayList of strings for list items
    undoStack: A stack of UndoCommand references for undo commands

Note that the addWithUndo() method is already implemented. The method adds a new item to the list and pushes a new RemoveLastCommand object onto the undo stack.

Step 3: Implement RemoveLastCommand's execute() method

The RemoveLastCommand class inherits from UndoCommand and is declared in RemoveLastCommand.java. When a RemoveLastCommand object is executed, the string ArrayList's last element is removed. So when the user appends a new item to the grocery list, a RemoveLastCommand is pushed onto the stack of undo commands. Popping and executing the RemoveLastCommand then removes the item most recently added by the user.

RemoveLastCommand's sourceList field and constructor are already declared:

    sourceList is a reference to a GroceryList object's ArrayList of strings.
    The constructor has an ArrayList of strings parameter and assigns sourceList with the ArrayList.

Implement RemoveLastCommand's execute() method to remove sourceList's last element.

Step 4: Implement GroceryList's executeUndo() method

Implement GroceryList's executeUndo() method to do the following:

    Pop an UndoCommand off the undo stack
    Execute the popped undo command

Main.java has some test methods. Each constructs a GroceryListTest object from a list of string commands. Test 1 tests code implemented so far: insertion and undo of insertion. Calls to other test methods are commented-out in main(). Run your code and make sure that test 1 passes before proceeding.

Step 5: Implement the SwapCommand class and GroceryList's swapWithUndo() method

Implement the SwapCommand class in SwapCommand.java. The class itself is declared, but with no members. Add necessary fields and methods so that the command can undo swapping two items in the grocery list.

Implement GroceryList's swapWithUndo() method. The method swaps list items at the specified indices, then pushes a SwapCommand to undo that swap onto the undo stack.

Uncomment the two lines in main() that call test2() and display results. Run your code and make sure that both test 1 and test 2 pass.

Step 6: Implement the InsertAtCommand class and GroceryList's removeAtWithUndo() method

Implement the InsertAtCommand class in InsertAtCommand.java. Add necessary fields and methods so that the command can undo removing a grocery list item at an arbitrary index.

Implement GroceryList's removeAtWithUndo() method. The method removes the list item at the specified index, then pushes an InsertAtCommand to undo that removal onto the undo stack.

Uncomment the two lines in main() that call test3() and display results. Run your code and make sure that all tests pass. The output from main() does not affect grading, so consider adding more tests to main() before submitting code.

Submit your code for grading.
