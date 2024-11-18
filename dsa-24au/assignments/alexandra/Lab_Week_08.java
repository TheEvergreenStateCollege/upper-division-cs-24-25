import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.IOException;
import java.util.ArrayList;

public class ReadData {
    static class Leaderboard {
        int speedrun_time;
        String speedrunner_username;
        String date_time_set;
        public Leaderboard() {
            this.speedrun_time = -1;
            this.speedrunner_username = null;
            this.date_time_set = null;
        }
    }
    public static void main(String args[]) {
        String filePath = "./MOCK_DATA.csv";
        try (BufferedReader br = new BufferedReader(new FileReader(csvFilePath))) {
            String line;
            boolean isHeaderSkipped = false;
            ArrayList<Leaderboard> leaderboardList = new ArrayList<>();
            while ((line = br.readLine()) != null) 
            {
                String[] tokens = line.toUpperCase().replace(" ", "_").split(",");
                if (tokens.length == 0 || line.length() == 0) 
                {
                    continue;
                }
                if (!isHeaderSkipped) 
                {
                    isHeaderSkipped = true;
                    continue; 
                }
                try 
                {
                    // assume formating is correct 
                    int id = Integer.parseInt(tokens[0]);
                    BunType bun = BunType.valueOf(tokens[1]);
                    PattyType patty = PattyType.valueOf(tokens[2]);

                    Sandwich s = new Sandwich(bun, patty);
                    orderList.add(s);

                } catch (IndexOutOfBoundsException | NumberFormatException e) 
                {
                    System.out.println("Error parsing line: " + line);
                    e.printStackTrace();
                }
        } catch (IOException ioe) 
        {
            System.err.println(ioe.toString());
        }
    }
}