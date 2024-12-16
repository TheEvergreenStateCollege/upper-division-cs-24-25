import java.util.*;

public class Tests {
   public static boolean testGetScoreAndSetScore() {
      System.out.print("\n");
      System.out.print("---- testGetScoreAndSetScore() ----");
      System.out.print("\n");

      // Create a gradebook with sample data for testing
      CourseGradebook gradebook = TestUtility.makeSampleGradebook();

      // Each test case is a (assignmentName, studentID, expectedScore) Tuple
      ArrayList<Tuple<String, Integer, Double>> testCases = new ArrayList<Tuple<String, Integer, Double>>(
            Arrays.asList(new Tuple<String, Integer, Double>("Midterm", 11111, 91.0),
                  new Tuple<String, Integer, Double>("Homework 1", 22222, Double.NaN),
                  new Tuple<String, Integer, Double>("Homework 3", 55555, 71.5),
                  new Tuple<String, Integer, Double>("Course project", 66666, 0.0),
                  new Tuple<String, Integer, Double>("Homework 2", 10000, 90.0),
                  new Tuple<String, Integer, Double>("Homework 4", 55555, 77.5),
                  new Tuple<String, Integer, Double>("Homework 5", 33333, Double.NaN),
                  new Tuple<String, Integer, Double>("Final exam", 44444, Double.NaN),
                  new Tuple<String, Integer, Double>("Homework 2", 77777, 76.0),
                  new Tuple<String, Integer, Double>("Homework 1", 88888, 64.5)));

      // Iterate through test cases
      for (var testCase : testCases) {
         String assignmentName = testCase.var0;
         Integer studentID = testCase.var1;
         Double expected = testCase.var2;
         Double actual = gradebook.getScore(assignmentName, studentID);

         // Reminder: Can't compare NaN with ==, so a special case is needed
         boolean areEqual = expected.isNaN() ? actual.isNaN() : (Double.compare(actual, expected) == 0);

         if (areEqual) {
            System.out.print("PASS: getScore(\"");
            System.out.print(assignmentName);
            System.out.print("\", ");
            System.out.print(studentID);
            System.out.print(") returned ");
            System.out.print(actual);
            System.out.print("\n");
         }
         else {
            System.out.print("FAIL: getScore(\"");
            System.out.print(assignmentName);
            System.out.print("\", ");
            System.out.print(studentID);
            System.out.print(") returned ");
            System.out.print(actual);
            System.out.print(", but expected is ");
            System.out.print(expected);
            System.out.print("\n");
            return false;
         }
      }
      return true;
   }

   public static boolean testGetAssignmentScores() {
      System.out.print("\n");
      System.out.print("---- testGetAssignmentScores() ----");
      System.out.print("\n");

      // Create a gradebook with sample data for testing
      CourseGradebook gradebook = TestUtility.makeSampleGradebook();

      HashMap<Integer, Double> hw2Scores = new HashMap<Integer, Double>() {
         {
            put(11111, 89.0);
            put(22222, 75.0);
            put(33333, 100.0);
            put(44444, 50.0);
            put(55555, 76.5);
            put(66666, 84.5);
            put(77777, 76.0);
            put(88888, 74.5);
            put(99999, 100.0);
            put(10000, 90.0);
            put(90000, 85.0);
         }
      };
      HashMap<Integer, Double> midtermScores = new HashMap<Integer, Double>() {
         {
            put(11111, 91.0);
            put(22222, 77.5);
            put(33333, 88.0);
            put(44444, 40.0);
            put(55555, 64.5);
            put(66666, 91.0);
            put(77777, 75.0);
            put(88888, 88.0);
            put(99999, 88.0);
            put(10000, 92.0);
            put(90000, 90.0);
         }
      };
      HashMap<Integer, Double> projectScores = new HashMap<Integer, Double>() {
         {
            put(11111, 100.0);
            put(22222, 60.0);
            put(33333, 90.0);
            put(55555, 87.0);
            put(66666, 0.0);
            put(77777, 72.0);
            put(88888, 85.5);
            put(99999, 80.0);
            put(10000, 77.5);
            put(90000, 85.0);
         }
      };

      // Each test case is a (assignmentName, mapOfExpectedScores) Pair
      ArrayList<Pair<String, HashMap<Integer, Double>>> testCases = new ArrayList<Pair<String, HashMap<Integer, Double>>>(
            Arrays.asList(new Pair<String, HashMap<Integer, Double>>("Homework 2", hw2Scores),
                  new Pair<String, HashMap<Integer, Double>>("Midterm", midtermScores),
                  new Pair<String, HashMap<Integer, Double>>("Course project", projectScores)));

      // Iterate through all test cases
      for (var testCase : testCases) {
         String assignmentName = testCase.var0;
         HashMap<Integer, Double> expectedMap = testCase.var1;

         // Get the actual map from the gradebook
         System.out.print("Calling getAssignmentScores(\"");
         System.out.print(assignmentName);
         System.out.print("\")");
         System.out.print("\n");
         HashMap<Integer, Double> actualMap = gradebook.getAssignmentScores(assignmentName);

         // Compare sizes first
         if (expectedMap.size() != actualMap.size()) {
            System.out.print("FAIL: getAssignmentScores(\"");
            System.out.print(assignmentName);
            System.out.print("\") returned a map with ");
            if (1 == actualMap.size()) {
               System.out.print("1 score, ");
            }
            else {
               System.out.print(actualMap.size());
               System.out.print(" scores, ");
            }
            System.out.print("but the expected map has ");
            System.out.print(expectedMap.size());
            System.out.print(" scores");
            System.out.print("\n");
            return false;
         }

         // Sizes are equal, so now compare each ID/score pair
         for (Integer key : expectedMap.keySet()) {
            Integer studentID = key;
            if (!actualMap.containsKey(studentID)) {
               System.out.print("FAIL: getAssignmentScores(\"");
               System.out.print(assignmentName);
               System.out.print("\") returned a map that is missing an entry ");
               System.out.print("for student ID ");
               System.out.print(studentID);
               System.out.print("\n");
               return false;
            }

            // Actual map has student ID, so now compare corresponding score
            Double expectedScore = expectedMap.get(key);
            Double actualScore = actualMap.get(studentID);
            boolean areEqual = expectedScore.isNaN() ? actualScore.isNaN()
                  : (Double.compare(actualScore, expectedScore) == 0);
            if (!areEqual) {
               System.out.print("FAIL: getAssignmentScores(\"");
               System.out.print(assignmentName);
               System.out.print("\") returned a map that has a score of ");
               System.out.print(actualScore);
               System.out.print(" for student ID ");
               System.out.print(studentID);
               System.out.print(", but the expected score is ");
               System.out.print(expectedScore);
               System.out.print("\n");
               return false;
            }
         }

         // All entries match
         System.out.print("PASS: getAssignmentScores(\"");
         System.out.print(assignmentName);
         System.out.print("\") returned a map with ");
         System.out.print(actualMap.size());
         System.out.print(" correct scores");
         System.out.print("\n");
      }
      return true;
   }

   public static boolean testGetSortedAssignmentNames() {
      System.out.print("\n");
      System.out.print("---- testGetSortedAssignmentNames() ----");
      System.out.print("\n");
      CourseGradebook gradebook = TestUtility.makeSampleGradebook();

      ArrayList<String> expected = new ArrayList<String>(Arrays.asList("Course project", "Final exam", "Homework 1",
            "Homework 2", "Homework 3", "Homework 4", "Midterm"));
      ArrayList<String> actual = gradebook.getSortedAssignmentNames();

      boolean areEqual = true;
      if (actual.size() == expected.size()) {
         // Compare elements in order
         for (int i = 0; areEqual && i < expected.size(); i++) {
            if (!expected.get(i).equals(actual.get(i))) {
               areEqual = false;
            }
         }
      }
      else {
         areEqual = false;
      }

      // Show pass or fail message along with expected and actual ArrayList contents
      if (areEqual) {
         System.out.print("PASS: getSortedAssignmentNames()");
         System.out.print("\n");
      }
      else {
         System.out.print("FAIL: getSortedAssignmentNames()");
         System.out.print("\n");
      }
      System.out.print("  Expected: ");
      System.out.println(expected);
      System.out.print("  Actual:   ");
      System.out.println(actual);

      return areEqual;
   }

   public static boolean testGetSortedStudentIDs() {
      System.out.print("\n");
      System.out.print("---- testGetSortedStudentIDs() ----");
      System.out.print("\n");
      CourseGradebook gradebook = TestUtility.makeSampleGradebook();

      ArrayList<Integer> expected = new ArrayList<Integer>(
            Arrays.asList(10000, 11111, 22222, 33333, 44444, 55555, 66666, 77777, 88888, 90000, 99999));
      ArrayList<Integer> actual = gradebook.getSortedStudentIDs();

      boolean areEqual = true;
      if (actual.size() == expected.size()) {
         // Compare elements in order
         for (int i = 0; areEqual && i < expected.size(); i++) {
            if (Integer.compare(actual.get(i), expected.get(i)) != 0) {
               areEqual = false;
            }
         }
      }
      else {
         areEqual = false;
      }

      // Show pass or fail message along with expected and actual ArrayList contents
      if (areEqual) {
         System.out.print("PASS: getSortedStudentIDs()");
         System.out.print("\n");
      }
      else {
         System.out.print("FAIL: getSortedStudentIDs()");
         System.out.print("\n");
      }
      System.out.print("  Expected: ");
      System.out.println(expected);
      System.out.print("  Actual:   ");
      System.out.println(actual);

      return areEqual;
   }

   public static boolean testGetStudentScores() {
      System.out.print("\n");
      System.out.print("---- testGetStudentScores() ----");
      System.out.print("\n");
      CourseGradebook gradebook = TestUtility.makeSampleGradebook();

      HashMap<String, Double> student22222Scores = new HashMap<String, Double>() {
         {
            put("Homework 2", 75.0);
            put("Midterm", 77.5);
            put("Homework 3", 80.5);
            put("Homework 4", 81.0);
            put("Course project", 60.0);
            put("Final exam", 54.0);
         }
      };
      HashMap<String, Double> student44444Scores = new HashMap<String, Double>() {
         {
            put("Homework 1", 60.0);
            put("Homework 2", 50.0);
            put("Midterm", 40.0);
            put("Homework 3", 30.0);
         }
      };
      HashMap<String, Double> student88888Scores = new HashMap<String, Double>() {
         {
            put("Homework 1", 64.5);
            put("Homework 2", 74.5);
            put("Midterm", 88.0);
            put("Homework 3", 84.0);
            put("Homework 4", 84.0);
            put("Course project", 85.5);
            put("Final exam", 81.5);
         }
      };
      HashMap<String, Double> student90000Scores = new HashMap<>() {
         {
            put("Homework 1", 80.0);
            put("Homework 2", 85.0);
            put("Midterm", 90.0);
            put("Homework 3", 95.0);
            put("Homework 4", 100.0);
            put("Course project", 85.0);
            put("Final exam", 94.5);
         }
      };

      // Each test case is a (studentID, mapOfExpectedScores) Pair
      ArrayList<Pair<Integer, HashMap<String, Double>>> testCases = new ArrayList<Pair<Integer, HashMap<String, Double>>>(
            Arrays.asList(new Pair<Integer, HashMap<String, Double>>(22222, student22222Scores),
                  new Pair<Integer, HashMap<String, Double>>(44444, student44444Scores),
                  new Pair<Integer, HashMap<String, Double>>(88888, student88888Scores),
                  new Pair<Integer, HashMap<String, Double>>(90000, student90000Scores)));

      // Iterate through all test cases
      for (var testCase : testCases) {
         Integer studentID = testCase.var0;
         HashMap<String, Double> expectedMap = testCase.var1;

         // Get the actual map from the gradebook
         System.out.println("Calling getStudentScores(" + studentID + ")");
         HashMap<String, Double> actualMap = gradebook.getStudentScores(studentID);

         // Compare sizes first
         if (expectedMap.size() != actualMap.size()) {
            System.out.print("FAIL: getStudentScores(");
            System.out.print(studentID);
            System.out.print(") returned a map with ");
            if (1 == actualMap.size()) {
               System.out.print("1 score, ");
            }
            else {
               System.out.print(actualMap.size());
               System.out.print(" scores, ");
            }
            System.out.print("but the expected map has ");
            System.out.print(expectedMap.size());
            System.out.println(" scores");
            return false;
         }

         // Sizes are equal, so now compare each assignment name/score pair
         for (String key : expectedMap.keySet()) {
            String assignmentName = key;
            if (!actualMap.containsKey(assignmentName)) {
               System.out.print("FAIL: getStudentScores(" + studentID);
               System.out.print(") returned a map that is missing an entry for ");
               System.out.println("assignment \"" + assignmentName + "\"");
               return false;
            }

            // Actual map has assignment name, so now compare corresponding score
            Double expectedScore = expectedMap.get(key);
            Double actualScore = actualMap.get(assignmentName);
            boolean areEqual = expectedScore.isNaN() ? actualScore.isNaN()
                  : (Double.compare(actualScore, expectedScore) == 0);
            if (!areEqual) {
               System.out.print("FAIL: getStudentScores(" + studentID);
               System.out.print(") returned a map that has a score of ");
               System.out.print(actualScore + " for assignment \"" + assignmentName);
               System.out.println("\", but the expected score is " + expectedScore);
               return false;
            }
         }

         // All entries match
         System.out.print("PASS: getStudentScores(" + studentID);
         System.out.print(") returned a map with ");
         System.out.println(actualMap.size() + " correct scores");
      }
      return true;
   }
}

// Basic Pair class for test cases
class Pair<T, U> {
   public T var0;
   public U var1;

   public Pair(T x, U y) {
      var0 = x;
      var1 = y;
   }
}

// Basic Tuple class for test cases
class Tuple<T, U, V> {
   public T var0;
   public U var1;
   public V var2;

   public Tuple(T x, U y, V z) {
      var0 = x;
      var1 = y;
      var2 = z;
   }
}