// Donna Quach
// DSA Week 10 Final Project 

import java.util.Scanner;   // To get user's input of their search parameters 

public class App {
    public static void main(String[] args) {
        Scanner userInput = new Scanner(System.in);
        System.out.print("Enter Make of Electric Vehicle: ");
        String vehicleMake = userInput.nextLine();
        System.out.print("Enter Model of Electric Vehicle: ");
        String vehicleModel = userInput.nextLine();
        System.out.println("Model and Make entered by user: " + vehicleMake + ' ' + vehicleModel); 
    }
}