import java.util.*;

public class TestUtility {
   // Populates a CourseGradebook from an ArrayList of rows. Each row is an
   // ArrayList
   // of Strings. Row 0 must be the header row. Column 0 must be the student ID
   // column.
   public static void populateGradebookFromRows(CourseGradebook gradebook, final ArrayList<ArrayList<String>> rows) {

      // Iterate through non-header rows
      for (int rowIndex = 1; rowIndex < rows.size(); rowIndex++) {
         var row = rows.get(rowIndex);

         // Parse out student ID first
         int studentID = Integer.parseInt(row.get(0));

         // Call setScore() for each non-empty entry
         for (int colIndex = 1; colIndex < row.size(); colIndex++) {
            String entry = row.get(colIndex);
            if (entry.length() > 0) {
               // Get the assignment name from the header row
               String assignmentName = rows.get(0).get(colIndex);

               // Convert score from string to double
               double score = Double.parseDouble(entry);

               // Add to gradebook
               gradebook.setScore(assignmentName, studentID, score);
            }
         }
      }
   }

   // Returns a sample gradebook to use for testing purposes.
   public static CourseGradebook makeSampleGradebook() {
      ArrayList<ArrayList<String>> rows = new ArrayList<ArrayList<String>>() {
         {
            add(new ArrayList<String>(Arrays.asList("Student ID", "Homework 1", "Homework 2", "Midterm", "Homework 3",
                  "Homework 4", "Course project", "Final exam")));
            add(new ArrayList<String>(Arrays.asList("11111", "92", "89", "91", "100", "100", "100", "95")));
            add(new ArrayList<String>(Arrays.asList("22222", "", "75", "77.5", "80.5", "81", "60", "54")));
            add(new ArrayList<String>(Arrays.asList("33333", "100", "100", "88", "100", "100", "90", "77.5")));
            add(new ArrayList<String>(Arrays.asList("44444", "60", "50", "40", "30", "", "", "")));
            add(new ArrayList<String>(Arrays.asList("55555", "73.5", "76.5", "64.5", "71.5", "77.5", "87", "63.5")));
            add(new ArrayList<String>(Arrays.asList("66666", "82.5", "84.5", "91", "92.5", "86", "0", "97")));
            add(new ArrayList<String>(Arrays.asList("77777", "77", "76", "75", "74", "73", "72", "71")));
            add(new ArrayList<String>(Arrays.asList("88888", "64.5", "74.5", "88", "84", "84", "85.5", "81.5")));
            add(new ArrayList<String>(Arrays.asList("99999", "100", "100", "88", "100", "100", "80", "79")));
            add(new ArrayList<String>(Arrays.asList("10000", "88", "90", "92", "87", "88.5", "77.5", "90")));
            add(new ArrayList<String>(Arrays.asList("90000", "80", "85", "90", "95", "100", "85", "94.5")));
         }
      };

      CourseGradebook gradebook = new CourseGradebook();
      populateGradebookFromRows(gradebook, rows);
      return gradebook;
   }
}