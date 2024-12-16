import java.util.*;

public class CourseGradebook extends Gradebook {
   // TODO: Declare any protected fields here (change placeholder field below)
   protected Map<String, HashMap<Integer, Double>> scoresByAsst = new HashMap<>();
   protected Map<Integer, HashMap<String, Double>> scoresByStudent = new HashMap<>();
   protected SortedSet<Integer> studentIds = new TreeSet<>();
   protected SortedSet<String> assignmentNames = new TreeSet<>();

   @Override
   public void setScore(String assignmentName, Integer studentID, Double score) {
      HashMap<Integer, Double> scores = scoresByAsst.get(assignmentName);
      HashMap<String,Double> scores2 = scoresByStudent.get(studentID);
      if (scores != null) {
        scores.put(studentID, score);
      } else {
        scores = new HashMap<Integer,Double>();
        scores.put(studentID, score);
      }
      scoresByAsst.put(assignmentName, scores);

      if (scores2 != null) {
        scores2.put(assignmentName, score);
      } else {
        scores2 = new HashMap<String,Double>();
        scores2.put(assignmentName, score);
      }
      scoresByStudent.put(studentID, scores2);

      studentIds.add(studentID);
   }

   @Override
   public double getScore(String assignmentName, Integer studentID) {
      Map<Integer, Double> scores = scoresByAsst.get(assignmentName);
      Double score = Double.NaN;
      if (scores != null) {
        Double score2 = scores.get(studentID);
        if (score2 != null) {
            score = score2;
        }
      } 
      return score;
   }

   @Override
   public HashMap<Integer, Double> getAssignmentScores(String assignmentName) {
      return scoresByAsst.get(assignmentName);
   }
   
   @Override
   public ArrayList<String> getSortedAssignmentNames() {
      // TODO: Type your code here (remove placeholder line below)
      ArrayList<String> results = new ArrayList<>();
      assignmentNames.forEach(name -> results.add(name));
      return results;
   }

   @Override
   public ArrayList<Integer> getSortedStudentIDs() {
      // TODO: Type your code here (remove placeholder line below)
      ArrayList<Integer> results = new ArrayList<>();
      studentIds.forEach(id -> results.add(id));
      return results;
   }

   @Override
   public HashMap<String, Double> getStudentScores(Integer studentID) {
      return scoresByStudent.get(studentID);
   }
}