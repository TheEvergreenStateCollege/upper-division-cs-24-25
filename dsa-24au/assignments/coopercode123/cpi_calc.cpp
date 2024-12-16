/*
* INFLATION CALCULATOR
* Scans in data from the CSV file and organizes it into a class
* Then the user can input commands that would call elements from the class and either display them or calculate with them
* Goes until the user tells the program to quit, for more information check the readme
*/

#include <iostream>
#include <cmath>
#include <fstream>
#include <sstream>
#include <cctype>
#include <iomanip>

            //Since using namespace std is a massive no no, idk why they even taught it to us lol
using std::cout;

//Pretty much everything is gonna need this even for how tedious it is lol
int monthToIndex(std::string month){
   int index;
   if(month == "January"){
      index = 0;
   }
   else if(month == "Febuary"){
      index = 1;
   }
   else if(month == "March"){
      index = 2;
   }
   else if(month == "April"){
      index = 3;
   }
   else if(month == "May"){
      index = 4;
   }
   else if(month == "June"){
      index = 5;
   }
   else if(month == "July"){
      index =6;
   }
   else if(month == "August"){
      index = 7;
   }
   else if(month == "September"){
      index = 8;
   }
   else if(month == "October"){
      index = 9;
   }
   else if(month == "November"){
      index = 10;
   }
   else if(month == "December"){
      index = 11;
   }
   else{
      index = 12;
   }
   return index;
}

            //Wasn't sure of good names to give these things
class itemInfo{
  private:
      std::string name;

            //Index 1: year, Index 2: Month
      double CPI[20][12];

            //Stores all yearly averages
      double yearlyAverage[20];

      public:

      void set_name (std::string input){
         name = input;
      }

      std::string get_name(){
         return name;
      }

      void set_CPI(int year_index, int month_index, double input_CPI){
         CPI[year_index][month_index] = input_CPI;
      }
      double get_CPI(int year_index, int month_index){
         return CPI[year_index][month_index];
      }

      //Caclulates the yaerly average, why not
      void calculate_yearly_average(){
         for(int i = 0; i < 20; i++){
            int n = 0;
            double sum = 0.000;
            for(int j = 0; j < 12; j++){
               //Handles the "no data"
               if(CPI[i][j] != 0){
               sum += CPI[i][j];
               n++;
               }
            }
         yearlyAverage[i] = sum / n;
         }
      }
      double get_yearly_average(int index){
         return yearlyAverage[index];
      }

            //Test function to ensure intilzation was done correctly
      void printObject(int year_index, int month_index){
            //cout << name << ", " << CPI[year_index][month_index] << '\n';
      }
};

int initData(itemInfo object[]){

   std::string readLine;
   int itr = 0;
   int index = 0;
            //For later
   std::string previousName;


   std::ifstream dataset("CPI_data.csv");
   if(dataset.is_open()){

      while(std::getline(dataset, readLine)){

            //Skips over the 1st row (basically just labels)
         if(itr == 0){
            itr++;
            continue;
         }

         std::istringstream ss(readLine);
         std::string words[4];
         std::string token;
         int year_index;
         int month_index;
         double hold_CPI;
         int n = 0;
            //cout << readLine << '\n';

            //Comparing new item
         while(std::getline(ss, token, ',')){
            words[n] = token;
            n++;
         }

         for(int i = 0; i < 4; i++){
            //cout << words[i] << '\n';
         }
         year_index = std::stoi(words[1]) - 2005;
         month_index = monthToIndex(words[2]);

         if(itr == 1){
            itr++;
            object[index].set_name(words[0]);
            previousName = words[0];
            object[index].set_CPI(year_index, month_index, hold_CPI);
            cout << previousName << '\n';
            continue;
         }

         if(words[0] != previousName){
            index++;
            object[index].set_name(words[0]);
            previousName = words[0];
            //Indicates when switch happens
            //cout << "New Name: " << previousName << '\n';
         }

         if(words[3].compare("None") != 0){
            hold_CPI = stod(words[3]);
            //cout << hold_CPI << '\n';
         }

            //Handles the none case, will put special case scenario to handle the zeros
         else{
            hold_CPI = 0.000;
         }

         object[index].set_CPI(year_index, month_index, hold_CPI);

            //Tests to ensure objects have properly intialized
            //cout << object[index].get_name() << " " << object[index].get_CPI(year_index, month_index) << '\n';

         std:ss.clear();
         }
   dataset.close();
            //Intalize yearly averages
   for(int i = 0; i < 19; i++){
      object[i].calculate_yearly_average();
            //        for(int j = 0; j < 20; j++){
            //            cout << object[i].get_name() << " average for " << j + 2005 << ": "<<object[i].get_yearly_average(j) << '\n';
            //         }
      }
   }

   else{
      cout << "ERROR, could not open file" << '\n';
      return 1;
   }
   return 0;
}

double calculate_inflation(double itemA, double itemB){
            //Inflation = (CPI_inital - CPI_current) / CPI_Current
return (itemA / itemB) / itemB;
}

            //Boring print functions who honestly cares lol
void print_aviable_items(){
   cout << "Items:" << '\n';
   cout << "1 - White Flour" << '\n';
   cout << "2 - Rice" << '\n';
   cout << "3 - Pasta" << '\n';
   cout << "4 - White Bread" << '\n';
   cout << "5 - Whole Bread" << '\n';
   cout << "6 - Cookies" << '\n';
   cout << "7 - Ground Beef" << '\n';
   cout << "8 - Roast Beef" << '\n';
   cout << "9 - Beef Steak" << '\n';
   cout << "10 -Pork Chops" << '\n';
   cout << "11 - Eggs" << '\n';
   cout << "12 - Milk" << '\n';
   cout << "13 - Cheddar Cheese" << '\n';
   cout << "14 - Ice Cream" << '\n';
   cout << "15 - Bananas" << '\n';
   cout << "16 - White Sugar" << '\n';
   cout << "17 - Potato Chips" << '\n';
   cout << "18 - Malt beverages" << '\n';
   cout << "19 - Wine" << '\n';
}

void print_command_list(){
   cout << "insert the number or character to start command." << '\n';
   cout << "1 - Shows the CPI for each month" << '\n';
   cout << "2 - Shows the average yearly CPI from 2005 to 2024" << '\n';
   cout << "3 - Calulates the inflation rate between the average of two years" << '\n';
   cout << "4 - Returns both minimum and maximum values for a given item across its entire set " << '\n';
   cout << "q - stops the program" << '\n';
   cout << "h - If you can't figure out what this does you probably should not be in a computer science class, let alone using this program :p" << '\n';
}

int check_input(char input){
switch (input){
case '1':
   return 1;
case '2':
   return 2;
case '3':
   return 3;
case '4':
   return 4;
case 'q':
   return 0;
case 'h':
print_command_list();
return 5;
default:
   cout <<"ERROR, UNKNOWN COMMAND, TRY AGIAN" << std::endl;
   cout << "What would you like to do? Type 'h' to see a list of commands" << '\n';
   return 5;
}
}

int main(){
   cout << std::fixed << std::showpoint;
   cout << std::setprecision(3);
   itemInfo object[19];
   if (initData(object) == 1){
   return -1;
   }
   else{

   int monthIndex1, monthIndex2;
   int yearIndex1, yearIndex2;
   int itemIndex;

   cout << "Data sucessfully intialized!" << '\n';
   char inputCommand;
   cout << "What would you like to do? Type 'h' to see a list of commands" << '\n';
   while(inputCommand != 'q'){
   std::cin >> inputCommand;
   switch (inputCommand){
   case '1':
      cout <<"Sorry, couldn't finish these in time, please end the session" << std::endl;
      continue;
   case '2':
      cout <<"Sorry, couldn't finish these in time, please end the session" << std::endl;
      continue;
   case '3':
      cout <<"Sorry, couldn't finish these in time, please end the session" << std::endl;
      continue;
   case '4':
      cout <<"Sorry, couldn't finish these in time, please end the session" << std::endl;
      continue;
   case 'q':
      cout << "Ending session, goodbye" << std::endl;
      break;

   case 'h':
   print_command_list();
   continue;

   default:
      cout <<"ERROR, UNKNOWN COMMAND, TRY AGIAN" << std::endl;
      cout << "What would you like to do? Type 'h' to see a list of commands" << '\n';
      continue;
   }
   }
}
return 0;
}
