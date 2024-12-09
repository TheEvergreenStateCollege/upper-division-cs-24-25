import java.util.*;

public abstract class Gradebook {
   // getScore() returns the specified student's score for the specified
   // assignment. NaN is returned if either:
   // - the assignment does not exist in the gradebook, or
   // - the assignment exists but no score exists for the specified student.
   public abstract double getScore(String assignmentName, Integer studentID);

   // setScore() adds or updates a score in the gradebook.
   public abstract void setScore(String assignmentName, Integer studentID, Double score);

   // getAssignmentScores() returns a HashMap that maps a student ID to
   // the student's corresponding score for the specified assignment. An entry
   // exists in the returned map only if a score has been entered with the
   // setScore() function.
   public abstract HashMap<Integer, Double> getAssignmentScores(String assignmentName);

   // getSortedAssignmentNames() returns an ArrayList with all distinct assignment
   // names, sorted in ascending order.
   public abstract ArrayList<String> getSortedAssignmentNames();

   // getSortedStudentIDs() returns an ArrayList with all distinct student IDs,
   // sorted in ascending order.
   public abstract ArrayList<Integer> getSortedStudentIDs();

   // getStudentScores() gets all scores that exist in the gradebook for the
   // student whose ID matches the method parameter. getStudentScores()
   // returns a HashMap that maps an assignment name to the student's
   // corresponding score for that assignment.
   public abstract HashMap<String, Double> getStudentScores(Integer studentID);
}