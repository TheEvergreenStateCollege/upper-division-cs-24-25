import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.IOException;

public class ReadData {

    static class Person {

        int id;
        String first_name;
        String last_name;
        String email;
        double salary;

        public person(String first_name, String last_name, String email, double salary) {
            this.id = id;
            this.first_name = first_name;
            this.last_name = last_name;
            this.email = email;
            this.salary = salary;
        }
    }

    static class IngredientsInStock {
        
    }

    public static void main(String[] args){
        
        String csvFilePath = "../data/sandwich_data.csv";
        //InputStream is = ReadData.class.getClassLoader().getResourceAsStream(csvFilePath);

        //<> are blank cause it can type inference
        //related types. one references the other.
        //Supertype is list. Subtype is ArrayList
        List<Sandwich> orderList = new ArrayList<>();
    
        //try (BufferedReader br = new BufferedReader(new InputStreamReader(is))) {
        try (BufferedReader br = new BufferedReader(new FileReader(csvFilePath))) {
            String line;
            
            boolean isHeaderSkipped = false;

            while ((line = br.readLine()) != null) 
            {

                String[] tokens = line.toUpperCase().replace(" ", "_").split(",");



                //skip any 0 length lines
                if (tokens.length == 0 || line.length() == 0) 
                {
                    continue;
                }

                //skip first line that is coluoum headers
                if (!isHeaderSkipped) 
                {
                    isHeaderSkipped = true;
                    continue; 
                }
    
                // try to scan one line and add to the data structure 
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
            } // while()
    
        } catch (IOException ioe) 
        {
            System.err.println(ioe.toString());
        }
    } // loadData()

}
