Seating Arrangements
There are n guests attending a dinner party, numbered from 1 to n. The ith guest has a height of arr[i-1] inches.
The guests will sit down at a circular table which has n seats, numbered from 1 to n in clockwise order around the table. As the host, you will choose how to arrange the guests, one per seat. Note that there are n! possible permutations of seat assignments.
Once the guests have sat down, the awkwardness between a pair of guests sitting in adjacent seats is defined as the absolute difference between their two heights. Note that, because the table is circular, seats 1 and n are considered to be adjacent to one another, and that there are therefore n pairs of adjacent guests.
The overall awkwardness of the seating arrangement is then defined as the maximum awkwardness of any pair of adjacent guests. Determine the minimum possible overall awkwardness of any seating arrangement.
Signature
int minOverallAwkwardness(int[] arr)
Input
n is in the range [3, 1000].
Each height arr[i] is in the range [1, 1000].
Output
Return the minimum achievable overall awkwardness of any seating arrangement.
Example
n = 4
arr = [5, 10, 6, 8]
output = 4
If the guests sit down in the permutation [3, 1, 4, 2] in clockwise order around the table (having heights [6, 5, 8, 10], in that order), then the four awkwardnesses between pairs of adjacent guests will be |6-5| = 1, |5-8| = 3, |8-10| = 2, and |10-6| = 4, yielding an overall awkwardness of 4. It's impossible to achieve a smaller overall awkwardness.

1

import java.util.*;

2

// Add any extra import statements you may need here

3

​

4

​

5

class Main {

6

​

7

  // Add any helper functions you may need here

8

  

9

​

10

  int minOverallAwkwardness(int[] arr) {

11

    // Write your code here

12

    

13

  }

14

​

15

​

16

​

17

​

18

​

19

​

20

​

21

​

22

​

23

​

24

​

25

​

26

  // These are the tests we use to determine if the solution is correct.

27

  // You can add your own at the bottom.

28

  int test_case_number = 1;

29

  void check(int expected, int output) {

30

    boolean result = (expected == output);

31

    char rightTick = '\u2713';

32

    char wrongTick = '\u2717';

33

    if (result) {

34

      System.out.println(rightTick + " Test #" + test_case_number);

35

    }

36

    else {

37

      System.out.print(wrongTick + " Test #" + test_case_number + ": Expected ");

38

      printInteger(expected); 

39

      System.out.print(" Your output: ");

40

      printInteger(output);

41

      System.out.println();

42

    }

43

    test_case_number++;

44

  }

45

  void printInteger(int n) {

46

    System.out.print("[" + n + "]");

47

  }

48

  

49

  public void run() {

50

    int[] arr_1 = {5, 10, 6, 8};

51

    int expected_1 = 4;

52

    int output_1 = minOverallAwkwardness(arr_1);

53

    check(expected_1, output_1);

54

​

55

    int[] arr_2 = {1, 2, 5, 3, 7};

56

    int expected_2 = 4;

57

    int output_2 = minOverallAwkwardness(arr_2);

58

    check(expected_2, output_2);

59

    

60

    // Add your own test cases here

61

    

62

  }

63

  

64

  public static void main(String[] args) {

65

    new Main().run();

66

  }

67

}

CONSOLE

Choose the programming language you're most comfortable with
Learn about this new feature
