import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.IOException;
import java.util.List;
import java.util.ArrayList;


public class ReadCSVData {

    static class Person {

        int id;
        String first_name;
        String last_name;
        String email;
        String gender;
        String ip_address;

        public Person(int id, String first_name, String last_name, String email, String gender, String ip_address) {
            this.id = id;
            this.first_name = first_name;
            this.last_name= last_name;
            this.email = email;
            this.gender = gender;
            this.ip_address = ip_address;
        }
        public String toString() {
            return "Person{id=" + id + ", first_name='" + first_name + "', last_name='" + last_name + "', email='" + email + "', gender='" + gender + "', ip_address='" + ip_address + "'}";
        }
    }

    public static void main(String[] args){
        
        String csvFilePath = "/workspace/upper-division-cs-24-25/dsa-24au/assignments/Quinn207/MOCK_DATA.csv";
        //InputStream is = ReadData.class.getClassLoader().getResourceAsStream(csvFilePath);

        List<Person> personList = new ArrayList<>();
    
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
                    String first_name = tokens[1];
                    String last_name = tokens[2];
                    String email = tokens[3];
                    String gender = tokens[4];
                    String ip_address = tokens[5];
                    

                    Person person = new Person(id, first_name, last_name, email, gender, ip_address);
                    personList.add(person);

                } catch (IndexOutOfBoundsException | NumberFormatException e) 
                {
                    System.out.println("Error parsing line: " + line);
                    e.printStackTrace();
                }
            }
    
        } catch (IOException ioe) {
        
            System.err.println(ioe.toString());
        
    } 
    personList.forEach(System.out::println);

}
}
