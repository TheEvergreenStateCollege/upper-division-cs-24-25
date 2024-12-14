// Donna Quach
// DSA Week 10 Final Project 

import java.io.File; // To read from CSV file 
import java.io.FileNotFoundException;
import java.util.Scanner;   // To get user's input of their search parameters 

public class App {
    public static void main(String[] args) {
        // Get user input 
        Scanner userInput = new Scanner(System.in);
        System.out.print("Enter Make of Electric Vehicle: ");
        String vehicleMake = userInput.nextLine();
        System.out.print("Enter Model of Electric Vehicle: ");
        String vehicleModel = userInput.nextLine();
        System.out.println("Model and Make entered by user: " + vehicleMake + ' ' + vehicleModel); 

        // Need to close Scanner object when finished getting user input 
        userInput.close(); 

        // Read from CSV file 
        // Source: https://www.w3schools.com/java/showjava.asp?filename=demo_files_read
        try {
            File myCSVFile = new File("Electric_Vehicle_Population_Data_20241111 (1).csv");
            Scanner theReader = new Scanner(myCSVFile);  
            while (theReader.hasNextLine()) {
              String data = theReader.nextLine();
              System.out.println(data);
            }
            // Need to close Scanner object when finished reading from CSV file 
            theReader.close();
          } 
        
        catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}