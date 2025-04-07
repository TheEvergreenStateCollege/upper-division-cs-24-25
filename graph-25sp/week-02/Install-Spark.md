# Graph Algorithms
Spring 2025

## Installing Spark

Spark is the processing engine we'll be using in our [textbook](https://www.oreilly.com/library/view/graph-algorithms/9781492047674/) and in this class to do data analytics
and see how they scale. While under the hood, Spark is implemented in Scala, a language in the Java Virtual Machine (JVM)
family of managed computing for its concurrency, parallelism, and powerful functional language features,
you can interface with it using Python (sometimes called PySpark), Scala, R, and also Java, which is
taught in the Backend Programming course sequence.

[Apache Spark Documentation](https://spark.apache.org)

## Desktop or Cloud?

While it's great to scale to datasets with billions and even millions of data items,
it's okay to start with thousands of data items that you can run on your laptop to start with.

![image](https://github.com/user-attachments/assets/72fd99ed-9139-4710-9be5-68764d43ecfc)

Then you can learn the basic principles and syntax, and you can do it offline (for example,
when you're on a plane, or at a family gathering where it's rude to keep asking for the wifi password).

To do this, follow the instructions in the textbook for installing and PySpark for Apache and Neo4j Desktop.

However, we are going to show the cloud version below with two servers (Spark worker nodes)
on our Digital Ocean account, which is a cloud platform like Amazon Web Services, Google Cloud, or Azure.

## Hello PySpark

In the traditions of our people, we must now run an introductory ritual to introduce you to Spark,
and that will be to autocreate a dataset of numbers from 1 to 1,000,000 and then count them.

This uses [a PySpark built-in method called `range`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.range.html) which takes one argument, the end position.

For example, if you run the function call

```
spark.range(5)
```

it should return

```
[0,1,2,3,4]
```

which as all computer science know, ends one before the specified bound, and starts at zero.
If instead you generated `[1,2,3,4,5]`, you should sign up for an electrical engineering class, or um, chemistry or something (just kidding).

There is a built-in function that counts the number of elements, which is the bound that is missing above, namely 5.

```
spark.range(5).count()
```

Now, 5 is not much of a stress test, and using the magic of "lazy evaluation" or "deferred execution"
that we'll learn about later, we can force the Spark and Scala to evaluate this all now by
calling `.count()`.

## Start PySpark

Change to where we've downloaded and extracted Spark+Hadoop
```
cd ~/spark-3.5.5-bin-hadoop3
JAVA_HOME=/root/.sdkman/candidates/java/17.0.9-graalce ./bin/pyspark
```

## Run Your First PySpark Task

After the prompt before, we'll type the following Python function
```
>>> def timed_count(x):
...     start = time.time()
...     result = spark.range(x*x*x).count()
...     elapsed = time.time() - start
...     print(f"Elapsed {elapsed}")
...
>>> import time
```

This Python function saves the current time, creates a Spark range as
discussed above, using the given argument `x`.

We "cube it up" by multiplying it by itself three times to get it
to scale faster to give us some interesting times. Try running it for
a few values of `x`.

>>> timed_count(10)
Elapsed 0.5855722427368164
>>> timed_count(100)
Elapsed 0.6240053176879883
>>> timed_count(1000)
```

Uh-oh, the first two values it handled with no sweat, however, these are
not the examples that big data folks live for.

It will often happen in graph algorithms work that we start a job that is
too big for our current hardware, or becomes a zombie that encounters
some where concurrency error, waits forever, or is way too slow given our
current approach, and we need to terminate the job and try again.

That's our next step.

## Spark Jobs Dashboard

Now, that we are hung up on a task that our seemingly mighty data processing engine cannot handle,
if only there was a way to tell what was going on.

Oh wait, there is! The Spark creators were nice enough to give us a website just
for managing past and current jobs, especially how long they have been running,
the command used to start them, and even killing them if necessary.

<img width="1388" alt="image" src="https://github.com/user-attachments/assets/af3a5d62-771c-4905-a6f0-c416709e59d4" />
