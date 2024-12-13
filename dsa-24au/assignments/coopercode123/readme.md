What dataset do you analyze? Are there multiple tables? For each table, answer what are the rows and what are the columns.
	- I analyzed the Consumer Price Index from 2005 to 2024 for 19 different items (source: https://www.bls.gov/regions/mid-atlantic/data/averageretailfoodandenergyprices_usandwest_table.html). The rows represent an individual item while the columns represent (going from left to right) the name of the item, the year, the month, and the CPI at that time.  
What questions is your software meant to answer on your dataset?

	- My software was actually meant to answer multiple questions, including inflation rates, how CPI has changed, what years have the highest CPI and inflation, what years have the lowest, inflation between two years, a bunch of stuff like that.

What algorithms and data structures did you use?
	-For algorithms I used a bit of string parsing when it came to breaking up the file lines to put each element into a class, and also used a sort of makeshift search algorithm for when converting the months to an actual index. As for data structures, there's a lot in there, classes, arrays, multidimensional arrays, stringstreams(if that counts).

What is their time and space complexity using big oh notation?

	- As for the functions, most of them are constant since its just a bunch of print statements or switch/else if statements. The ones that have slightly higher run time are the yearly average, which have a runtime of big O(i*j) and a space complexity of O(j). As for the monster of the initialization function, I believe the worst-case runtime would be O(n), where n is the amount of items in the dataset. Since all the other loops are consistent in the function and don't really change. The best-case would be O(1), meaning the file just was never read in. A similar case would occur with the space complexity, it all depends on how many items are read in (in my case a lot lol).

How can someone test your code? For example, what are some example inputs and the corresponding output you expect.
	-Can't traditionally test it since I wasn't able to get to the calculation parts, but what can be done is uncommenting some of the test lines I used during the initialization of the data to ensure everything initialized properly 

Consider what the command-line interface would be, or API requests and responses if you have a website.
	- Honestly the best thing I could think of would be doing multiple segments where you input stuff regarding what you want to calculate with the program. 

What challenges did you encounter and how did you solve them?
	-Many challenges, mainly initialization was the hardest part. I wasn't sure how to do it efficiently and decided to just initialize it at the start and read the data in once instead of doing it multiple times. Another issue I had that I wasn't able to fix in time was figuring out a 

What programming languages, frameworks, or technologies did you use?
	-I used C++ with the cmath, string, iomanip, ssstream, and fstream libraries. 

Who are your teammates, if any?
	-Worked Solo