public class Main {
   public static void main(String[] args) {
      boolean result1 = Tests.testGetScoreAndSetScore();
      boolean result2 = Tests.testGetAssignmentScores();
      boolean result3 = Tests.testGetSortedAssignmentNames();
      boolean result4 = Tests.testGetSortedStudentIDs();
      boolean result5 = Tests.testGetStudentScores();

      System.out.println();
      System.out.println("Summary:");
      System.out.println("testGetScoreAndSetScore(): " + (result1 ? "PASS" : "FAIL"));
      System.out.println("testGetAssignmentScores(): " + (result2 ? "PASS" : "FAIL"));
      System.out.println("testGetSortedAssignmentNames(): " + (result3 ? "PASS" : "FAIL"));
      System.out.println("testGetSortedStudentIDs(): " + (result4 ? "PASS" : "FAIL"));
      System.out.println("testGetStudentScores(): " + (result5 ? "PASS" : "FAIL"));
   }
}
