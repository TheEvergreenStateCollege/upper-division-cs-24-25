import java.io.BufferedReader;
import java.io.FileReader;
// import java.io.InputStreamReader;
// import java.io.InputStream;
import java.io.IOException;

public class ReadData {

    static class Sandwich {

        BunType bottomBun;
        BunType topBun;
        PattyType patty;

        public Sandwich(BunType bun, PattyType patty) {
            this.bottomBun = bun;
            this.topBun = bun;
            this.patty = patty;
        }
    }

    static class IngredientsInStock {

    }
  
    static enum BunType {
        POTATO,
        WHOLE_WHEAT,
        BRIOCHE,
        SESAME,
        PRETZEL,
    }

    static enum PattyType {
        CHICKEN,
        BEEF,
        TURKEY,

    }

    public static void main(String[] args){
        
        String csvFilePath = "../data/sandwich_data.csv";
        //InputStream is = ReadData.class.getClassLoader().getResourceAsStream(csvFilePath);

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

    Sandwich sandwich = new Sandwich(sandwichType, bunType, fillings, protein, sauce,
    toppings, spices, sideDish, drink, price);  //creating the sandwhich object

    sandwichList.add(sandwich);     //adding sandwhich to list
}
