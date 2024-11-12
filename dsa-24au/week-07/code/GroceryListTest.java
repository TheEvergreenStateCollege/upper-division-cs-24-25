import java.util.*;
import java.io.PrintWriter;

class GroceryListTest {
   // Stores a list of commands, each of which is one of the five forms:
   // - add itemName
   // - removeat index
   // - swap index1 index2
   // - undo
   // - verify listItem1,listItem2,...,lastListItem
   protected ArrayList<String> commands;

   protected boolean showCommands;
   protected boolean assertUndoCount;

   public GroceryListTest(ArrayList<String> commands) {
      this.commands = commands;
      showCommands = true;
      assertUndoCount = true;
   }

   protected boolean execCommand(String command, GroceryList groceryList, PrintWriter testFeedback) {

      // Record the undo stack size prior to executing the command
      int undoCountBefore = groceryList.getUndoStackSize();

      // Store the current undo stack size as the "expected" undo stack size.
      // The expected count is incremented for the add, removeat, and swap
      // commands, and is decremented for the undo command.
      int expectedUndoCount = groceryList.getUndoStackSize();

      // Check the command string
      if (0 == command.indexOf("add ")) {
         String itemToAdd = command.substring(4);
         if (showCommands) {
            testFeedback.println("Adding " + itemToAdd);
         }
         groceryList.addWithUndo(itemToAdd);
         expectedUndoCount++;
      }
      else if (0 == command.indexOf("removeat ")) {
         int index = Integer.parseInt(command.substring(9));
         if (showCommands) {
            testFeedback.println("Removing at index " + index);
         }
         groceryList.removeAtWithUndo(index);
         expectedUndoCount++;
      }
      else if (0 == command.indexOf("swap ")) {
         String whatToSwap = command.substring(5);
         int spaceIndex = whatToSwap.indexOf(" ");
         if (spaceIndex > 0) {
            int index1 = Integer.parseInt(whatToSwap.substring(0, spaceIndex));
            int index2 = Integer.parseInt(whatToSwap.substring(spaceIndex + 1));

            if (showCommands) {
               testFeedback.println("Swapping at indices " + index1 + " and " + index2);
            }

            groceryList.swapWithUndo(index1, index2);
         }
         else {
            testFeedback.println("Malformed swap command: " + command);
            return false;
         }
         expectedUndoCount++;
      }
      else if (command == "undo") {
         if (showCommands) {
            testFeedback.println("Executing undo");
         }

         if (0 == groceryList.getUndoStackSize()) {
            testFeedback.println("FAIL: Cannot execute undo because undo stack " + 
               "is empty");
         }
         else {
            groceryList.executeUndo();
         }
         expectedUndoCount--;
      }
      else if (0 == command.indexOf("verify ")) {
         String listStr = command.substring(7);
         String[] expected = listStr.split(",");
         String[] actual = groceryList.getItemList();
         if (!Arrays.equals(expected, actual)) {
            testFeedback.println("FAIL:");
            testFeedback.println("  Expected list: " + expected);
            testFeedback.println("  Actual list: " + actual);
            return false;
         }

         testFeedback.println("PASS: Verified list content: " + listStr);
      }
      else if (command.equals("verify")) {
         // Special case for empty list
         int actualSize = groceryList.getItemList().length;
         if (0 == actualSize) {
            testFeedback.println("PASS: List is empty");
         }
         else {
            testFeedback.println(
               "FAIL: List should be empty, but instead has " + actualSize + " item" + (1 == actualSize ? "" : "s"));
         }
      }

      // If the undo stack size should have changed, verify
      if (assertUndoCount && undoCountBefore != expectedUndoCount) {
         // Get the actual undo command count
         int actualCount = groceryList.getUndoStackSize();

         if (expectedUndoCount != actualCount) {
            testFeedback.println(
                  "FAIL: Expected undo stack size is " + expectedUndoCount + ", but actual size is " + actualCount);
            return false;
         }
         else {
            testFeedback.println("PASS: Undo stack size is " + actualCount);
         }
      }

      return true;
   }

   public boolean execute(PrintWriter testFeedback) {
      // Create a GroceryList
      GroceryList groceryList = new GroceryList();

      // Execute each command in the commands list
      for (String command : commands) {
         if (!execCommand(command, groceryList, testFeedback)) {
            return false;
         }
      }

      // All tests passed
      return true;
   }
}
