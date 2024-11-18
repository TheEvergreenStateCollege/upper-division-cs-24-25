import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ReadCSV {
    public static void main(String[] args) {
        String filePath = "/Users/queenofthedead/Downloads/MockSandwhichData.csv"; // File name
        String line;

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            while ((line = br.readLine()) != null) {
                System.out.println(line); // Print each line directly
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
