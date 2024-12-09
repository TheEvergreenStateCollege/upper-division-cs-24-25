Passing Yearbooks
There are n students, numbered from 1 to n, each with their own yearbook. They would like to pass their yearbooks around and get them signed by other students.
You're given a list of n integers arr[1..n], which is guaranteed to be a permutation of 1..n (in other words, it includes the integers from 1 to n exactly once each, in some order). The meaning of this list is described below.
Initially, each student is holding their own yearbook. The students will then repeat the following two steps each minute: Each student i will first sign the yearbook that they're currently holding (which may either belong to themselves or to another student), and then they'll pass it to student arr[i-1]. It's possible that arr[i-1] = i for any given i, in which case student i will pass their yearbook back to themselves. Once a student has received their own yearbook back, they will hold on to it and no longer participate in the passing process.
It's guaranteed that, for any possible valid input, each student will eventually receive their own yearbook back and will never end up holding more than one yearbook at a time.
You must compute a list of n integers output, whose element at i-1 is equal to the number of signatures that will be present in student i's yearbook once they receive it back.
Signature
int[] findSignatureCounts(int[] arr)
Input
n is in the range [1, 100,000].
Each value arr[i] is in the range [1, n], and all values in arr[i] are distinct.
Output
Return a list of n integers output, as described above.
Example 1
n = 2
arr = [2, 1]
output = [2, 2]
Pass 1:

    Student 1 signs their own yearbook. Then they pass the book to the student at arr[0], which is Student 2.
    Student 2 signs their own yearbook. Then they pass the book to the student at arr[1], which is Student 1.

Pass 2:

    Student 1 signs Student 2's yearbook. Then they pass it to the student at arr[0], which is Student 2.
    Student 2 signs Student 1's yearbook. Then they pass it to the student at arr[1], which is Student 1.

Pass 3:

    Both students now hold their own yearbook, so the process is complete.

Each student received 2 signatures.
Example 2
n = 2
arr = [1, 2]
output = [1, 1]
Pass 1:

    Student 1 signs their own yearbook. Then they pass the book to the student at arr[0], which is themself, Student 1.
    Student 2 signs their own yearbook. Then they pass the book to the student at arr[1], which is themself, Student 2.

Pass 2:

    Both students now hold their own yearbook, so the process is complete.

Each student received 1 signature.

```java
import java.io.*; 
import java.util.*;
// Add any extra import statements you may need here


class Main {

  // Add any helper functions you may need here
  

  int[] findSignatureCounts(int[] arr) {
    // Write your code here
    
  }












  // These are the tests we use to determine if the solution is correct.
  // You can add your own at the bottom.
  int test_case_number = 1;
  void check(int[] expected, int[] output) {
    int expected_size = expected.length; 
    int output_size = output.length; 
    boolean result = true; 
    if (expected_size != output_size) {
      result = false;
    }
    for (int i = 0; i < Math.min(expected_size, output_size); i++) {
      result &= (output[i] == expected[i]);
    }
    char rightTick = '\u2713';
    char wrongTick = '\u2717';
    if (result) {
      System.out.println(rightTick + " Test #" + test_case_number);  
    }
    else {
      System.out.print(wrongTick + " Test #" + test_case_number + ": Expected ");
      printIntegerArray(expected); 
      System.out.print(" Your output: ");
      printIntegerArray(output);
      System.out.println();
    }
    test_case_number++;
  }
  void printIntegerArray(int[] arr) {
    int len = arr.length; 
    System.out.print("[");
    for(int i = 0; i < len; i++) {
      if (i != 0) {
        System.out.print(", ");
      }
      System.out.print(arr[i]);
    }
    System.out.print("]");
  }
  
  public void run() {
    int[] arr_1 = {2, 1};
    int[] expected_1 = {2, 2};
    int[] output_1 = findSignatureCounts(arr_1);
    check(expected_1, output_1);
    
    int[] arr_2 = {1, 2};
    int[] expected_2 = {1, 1};
    int[] output_2 = findSignatureCounts(arr_2);
    check(expected_2, output_2);
  
    // Add your own test cases here
    
  }
  
  public static void main(String[] args) throws IOException {
    new Main().run();
  }
}
```
