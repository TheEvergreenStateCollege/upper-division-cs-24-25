# DSA Week 10 Final Project - Electric Vehicle Population Data (Thurston County)
What dataset do you analyze? Are there multiple tables? For each table, answer what are the rows and what are the columns.
    - My dataset consists of data on electric vehicles that are registered through the Washington State Department of Licensing. This dataset was published on data.wa.gov by the Washington State Department of Licensing. Each row represents an electric vehicle that is registered in the county. 
        a. Fields: VIN, County (Registered in), City, State, Postal Code, Model Year, Make, Model, Electric Vehicle Type, Clean Alternative Fuel Vehicle Eligibility, Electric Range, Legislative District, DOL Vehicle ID

What questions is your software meant to answer on your dataset?
    - What is the most common/popular Make that is registered in Thurston County? 
    - Of the most common Make, what is the most common Model? 

What algorithms and data structures did you use?
    - I used a while loop. 

What is their time and space complexity using big oh notation?
    - The while loop has a time complexity of O(n), and it has a space complexity of O(n). 

How can someone test your code? For example, what are some example inputs and the corresponding output you expect.
    - I think if this project were fully complete, then I would have compared the output of the program vs. the count within the CSV spreadsheet that was read from. The CSV spreadsheet will allow you to order the data based on the column selected. The spreadsheet can also provide you with the count too of certain makes and/or models. 

Consider what the command-line interface would be, or API requests and responses if you have a website.
    - If this project were connected to an API, a GET request would be used to pull the data and display to the user for viewing. 

What challenges did you encounter and how did you solve them?
    - Even though this was as far as I got with the project, I foresee a couple of challenges.
        - I will have to figure out how to go through the CSV and look at values that are part of the Make and/or Model columns in order to answer questions regarding my dataset. (To take the count of each model with the year and find which was owned the most.)
        - I will have to figure out how to pass in the values of the CSV to then have that data stored within an ArrayList. I believe I will have to create a separate class from the App class that will specifically handle the list itself. It would then theoretically return to the App class (main program) the electric car that is registered the most in Thurston County. 

What programming languages, frameworks, or technologies did you use?
    - This program uses only Java. 

Who are your teammates, if any?
    - I did not work with any teammates on this assignment. 