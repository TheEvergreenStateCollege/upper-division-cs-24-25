This is the writing in my part for [Torsten's soccer leaderboard](https://github.com/TheEvergreenStateCollege/upper-division-cs-24-25/tree/main/tps-24au/assignments/EvergreenTor/finalProject/src) project that we both worked together. The code is also included in one of his framework on his TPS HW folder followed the links. Since we also worked together on the [README.md](https://github.com/TheEvergreenStateCollege/upper-division-cs-24-25/blob/main/tps-24au/assignments/EvergreenTor/finalProject/src/README.md) for the project, any question that I might encounter here can also be answer through there as well.

1. What dataset do you analyze? Are there multiple tables? For each table, answer what are the rows and what are the columns.

We analyze a dataset that has 10000 different players entries, that spread across 10 different tables, with 1000 each to sort who's the best player in each table (that scored the most goals). The rows will be different players entries and the columns will be the different attributes of each player, consist of their name, age, team, position, nationalities, matches played, and goals scored.

2. What questions is your software meant to answer on your dataset?

It could be who's the best player for each year, represents as different tables. Or maybe which team has the most players in the top 10 or something like that.

3. What algorithms and data structures did you use?

We use a reimplementation of maxHeap to fit the requirement, there could also be other data structure in play such as hashmap or arraylist, behind the maxHeap one

4. What is their time and space complexity using big oh notation?

maxHeap by itself only took up O(n) or O(log n) for both space and time complexity. Consider that this is a reimplementation of maxHeap, the time complexity for it should stay the same. There might be some slight change on space complexity due to the reimplementation, but it should still be O(n) or O(log n)

5. How can someone test your code? For example, what are some example inputs and the corresponding output you expect.

This has been explained somewhat in the readme file but I can put it here for reference.

```
The command is "python3 main.py"
You'll show with the menu that has the following description:

Welcome to the soccer leaderboard. Choose an option:
1: Show leaderboard for 2015
2: Show leaderboard for 2016
3: Show leaderboard for 2017
4: Show leaderboard for 2018
5: Show leaderboard for 2019
6: Show leaderboard for 2020
7: Show leaderboard for 2021
8: Show leaderboard for 2022
9: Show leaderboard for 2023
10: Show leaderboard for 2024
0: quit
Enter a number:

From this point, choose any number from 1-10 and it will show the following leaderboard for that year

When you're finished, type 0 to quit the menu

Try typing any number outside of 0-10 to see something happens!

No characters are allowed except numbers
```

6. Consider what the command-line interface would be, or API requests and responses if you have a website.
What challenges did you encounter and how did you solve them?

It's mostly to make it functional without error and having a seemless experience. Torsten propose to use a switch statement to make it more readable and easier to understand. However it's a new feature on a newer version of python, which most other doesn't have, this leads to an error if you run a version lower than the version it needs. So I ended up make a condition check on the compiler, if the compiler is old, it will use the if else statement instead of the new switch statement.

7. What programming languages, frameworks, or technologies did you use?

We only use Python, with mock data from mockaroo.com

8. Who are your teammates, if any?

I worked with Torsten on this one. It was his idea to implement it and I also like to play soccer so that checks out both of us