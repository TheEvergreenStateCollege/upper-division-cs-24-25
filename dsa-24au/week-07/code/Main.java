import java.util.*;
import java.io.PrintWriter;

public class Main {

   public static void main(String[] args) {
      PrintWriter testFeedback = new PrintWriter(System.out);

      boolean test1Pass = test1(testFeedback);
      System.out.println("Test 1: " + (test1Pass ? "PASS" : "FAIL"));

      // boolean test2Pass = test2(testFeedback);
      // System.out.println("Test 2: " + (test2Pass ? "PASS" : "FAIL"));

      // boolean test3Pass = test3(testFeedback);
      // System.out.println("Test 3: " + (test3Pass ? "PASS" : "FAIL"));
   }

   // Test 1 tests insertion and undo of insertion only
   static boolean test1(PrintWriter testFeedback) {
      GroceryListTest test = new GroceryListTest(
         new ArrayList<String>(Arrays.asList("add carrots", "verify carrots", "undo", // undo addition of carrots
            "verify", // verify empty list
            "add potatoes", "verify potatoes", "add carrots", "verify potatoes,carrots", "add lettuce",
            "verify potatoes,carrots,lettuce", "add rice", "verify potatoes,carrots,lettuce,rice", "add cilantro",
            "verify potatoes,carrots,lettuce,rice,cilantro", "undo", // undo addition of cilantro
            "verify potatoes,carrots,lettuce,rice", "undo", // undo addition of rice
            "verify potatoes,carrots,lettuce", "undo", // undo addition of lettuce
            "verify potatoes,carrots", "undo", // undo addition of carrots
            "verify potatoes", "undo", // undo addition of potatoes
            "verify", "add basil", "vefify basil", "add onions", "vefify basil,onions", "add spinach",
            "vefify basil,onions,spinach", "undo", // undo addition of spinach
            "vefify basil,onions", "undo", // undo addition of onions
            "vefify basil", "undo", // undo addition of basil
            "verify")));
      return test.execute(testFeedback);
   }

   // Test 2 tests insertion and swapping and the undo of each
   static boolean test2(PrintWriter testFeedback) {
      GroceryListTest test = new GroceryListTest(
         new ArrayList<String>(Arrays.asList("add chips", "add cookies", "add waffles", "add syrup", "add ice cream",
            "add lettuce", "verify chips,cookies,waffles,syrup,ice cream,lettuce", "swap 1 4", // swap cookies and
                                                                                               // ice cream
            "verify chips,ice cream,waffles,syrup,cookies,lettuce", "undo", // undo the swap
            "verify chips,cookies,waffles,syrup,ice cream,lettuce")));
      return test.execute(testFeedback);
   }

   // Test 3 tests all commands
   static boolean test3(PrintWriter testFeedback) {
      GroceryListTest test = new GroceryListTest(new ArrayList<String>(
         Arrays.asList("add orange juice", "add apple juice", "verify orange juice,apple juice", "undo", // undo add
                                                                                                            // apple
                                                                                                            // juice
            "verify orange juice", "removeat 0", "verify", "undo", // undo remove orange juice
            "verify orange juice", "undo", // undo add orange juice
            "verify", "add mango juice", "verify mango juice", "add grapefruit juice", "add grape juice",
            "verify mango juice,grapefruit juice,grape juice", "swap 0 1",
            "verify grapefruit juice,mango juice,grape juice", "add strawberry smoothie",
            "verify grapefruit juice,mango juice,grape juice,strawberry smoothie", "swap 2 3",
            "verify grapefruit juice,mango juice,strawberry smoothie,grape juice", "removeat 3",
            "verify grapefruit juice,mango juice,strawberry smoothie", "removeat 1",
            "verify grapefruit juice,strawberry smoothie", "swap 0 1",
            "verify strawberry smoothie,grapefruit juice", "undo", // undo swap 0 1
            "undo", // undo removal of mango juice
            "undo", // undo removal of grape juice
            "undo", // undo swap 2 3
            "undo", // undo add strawberry smoothie
            "verify grapefruit juice,mango juice,grape juice", "undo", // undo swap 0 1
            "undo", // undo add grape juice
            "verify mango juice,grapefruit juice", "undo", // undo add grapefruit juice
            "verify mango juice", "undo", // undo add mango juice
            "verify")));
      return test.execute(testFeedback);
   }
}
