# Week 01

Functional Programming Simplified, by Alvin Alexander

## Readings

Chapters 1-14
*Scala Syntax and FP*

## Study Questions

Only attempt these questions *after* reading through each chapter.

### Chapter 1

*. What does FP stand for?

*. What's the relationship between Haskell, Scala, and FP?

### Chapter 2

*. Pick two of the five reasons to study FP and Scala listed in this chapter that most apply to you. Explain why.

### Chapter 3

*. Pick two of the six learning goals in this chapter that most appeal to you right now. Explain why.

### Chapter 4

No questions, but we'll come back to this in the future.

If you are curious about the [Big Scala Book]() after completing this course, many of this FP Simplified book will become beneficial.

### Chapter 5

No questions, but consider the attitude of the reporter.

### Chapter 6

* Pick one of the following and describe how it is an example of external input/output (I/O)?
  * [database](https://en.wikipedia.org/wiki/Database) code
  * [RESTful](https://en.wikipedia.org/wiki/REST) code
  * [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface) code

You may read the first paragraph of your chosen Wikipedia entry to learn enough about it to answer.

* How is critical thinking related to our discussion of imperative versus functional programming?

Sometimes you will encounter the term "declarative programming". This was a more popular style in the early
days of computing and is seeing a resurgence.

How is it related to functional programming?

Try typing this (imperative) code snippet from the book character-for-character into [Scastie](), an online playground for command-line Scala.

```
def sum(ints: List[Int]): Int = {
   var sum = 0
   for (i <- ints) {
      sum += i
   }
   sum
}

sum(List(1,2,3))
```

Look out for any red underlines that will explain syntax as you type, and when you're done, try running it by clicking the "Run" button.

Try a functional, recursive version, also in Scastie, and make sure they output the same answer.

Make sure it compiles and runs.

Hint: think of a base case and a recursive case, and search for a way to find the length of a list in Scala and index into the `i`th element of a list in Scala.
