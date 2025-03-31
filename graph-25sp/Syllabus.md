# Graph Algorithms in Scala

## Credits:
4 upper division computer science credits called
`Graph Algorithms in Scala, Python and Neo4j`
## Learning Goals
Learn and explain the basics of functional programming pros and cons with other styles
Recognize and explain fundamentals of Scala syntax and Scala implementations of some graph algorithms
Learn and explain basics of graph data structure
Describe some important graph algorithms and their applications
Run basic web visualizations of graphs with Scala.js and Laminar
## Textbooks:
Graph Algorithms in Spark and Neo4j  by Mark Needham and Amy Hodler
ISBN 9781492047681, May 2019 (Abbreviated `GraphSparkNeo4j` below)

Functional Programming Simplified by Alvin Alexander
ISBN 1979788782, December 2017 (Abbreviated `FP Simplified` below)
## Source Code:

#### FP Simplified / Alvin Alexander
(Complete list in the FP Simplified Book PDF)
https://github.com/alvinj/FPDebuggable
https://github.com/alvinj/FPTypeClassesWithCats
https://github.com/alvinj/FPLenses
https://github.com/alvinj/FPMonadTransformers
#### Graph Algos / Mark Needham
https://github.com/neo4j-graph-analytics/book

| Week | Topics                                                                                                                                | Readings                                                                                                                          | Evaluate                                                                                                                                                                                                                          |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 01   | Introduction to Functional Programming<br><br>Review of Graphs<br><br>Online Practice with <br>Scastie and<br>Scribble.ninja          | `FP Simplified`<br>Chapters 1-14<br>*Scala Syntax and FP*<br><br>`Graph Algos`<br>Chapter 1<br>pages 1-14                         | Explain the goals of FP and pros and cons of Scala, compared to Java, Python, C/C++<br><br>Discuss study questions: what are graphs, online transactions versus offline processing.                                               |
| 02   | Scala Syntax and Graph Algorithms                                                                                                     | `FP Simplified` Chapters 15-26 *Functions and Parameters*<br><br>`Graph Algos`<br>Chapter 2<br>pages 15-28                        | Explain and run simple Scala functions with parameters  types, generics, and return types.<br><br>Discuss study questions: types of graphs and properties, cyclic vs. acyclic, directed vs. undirected, types of graph algorithms |
| 03   | Recursion Review and in Scala<br><br>Installing Apache Spark and Neo4j on Digital Ocean                                               | `FP Simplified` Chapters 27-39 *Recursion*<br><br>`Graph Algos`<br>Chapter 3<br>pages 29-37                                       | Explain and run Scala examples of recursive functions.<br><br>Discuss study questions: pros and cons for Spark versus Neo4j                                                                                                       |
| 04   | Scala and FP iteration and generators<br><br>Translate breadth-first search, depth-first search, cycle-finding from Python into Scala | `FP Simplified` Chapters 40-51<br>*State, Mutability, For Loops*<br><br>`Graph Algos`<br>Chapter 4, part 1<br>pages 38-49         | Explain and run Scala examples of state, mutability, and for loops.<br><br>Explain and run BFS, DFS, and cycle-finding in Scala<br><br>Run example transport graph from European road network.<br><br>                            |
| 05   | Scala and FP options and flatmap<br><br>Translate single-pair shortest-path, A* and Yen's k-shortest Path from Python into Scala      | FP Simplified Chapters 52-61<br>*Exceptions, Options, flatMap*<br><br>`Graph Algos`<br>Chapter 4, part 2<br>pages 49-60           | Explain and run Scala examples for exceptions, options, flatMap<br><br>Explain and run single-pair shortest-path graph algos in Scala                                                                                             |
| 06   | Scala wrappers<br><br>Translate all-pairs shortest-path from Python into Scala                                                        | FP Simplified Chapters 62-72<br>*Apply, Bind, Wrapper, Debuggable*<br><br>`Graph Algos`<br>Chapter 4, part 3<br>pages 61-70       | Explain and run Scala examples for apply, bind, wrapper, debuggable<br><br>Explain and run all-pairs shortest-path graph algos in Scala                                                                                           |
| 07   | Scala monads, part 1<br><br>Translate minimum spanning tree and random walk from Python into Scala                                    | FP Simplified Chapters 73-86<br>*Monads, State Monad Source Code*<br><br>`Graph Algos`<br>Chapter 4, part 4<br>pages 70-76        | Explain and run Scala examples for monad and state monad<br><br>Explain and run MST and random walk graph algos in Scala                                                                                                          |
| 08   | Scala monads, part 2<br><br>Translate degree centrality from Python into Scala                                                        | FP Simplified Chapters 87-92<br>*Monads, Transformers, Part I*<br><br>`Graph Algos`<br>Chapter 5, part 1<br>pages 77-84           | Explain and run Scala examples for monads from readings.<br><br>Explain and run degree centrality graph algos in Scala                                                                                                            |
| 09   | Scala monads, part 3<br><br>Translate closeness centrality from Python into Scala                                                     | FP Simplified Chapters 93-99<br>*Monads, Transformers, Part II*<br><br>`Graph Algos`<br>Chapter 5, part 2<br>pages 84-92          | Explain and run Scala examples for monads from readings.<br><br>Run example social media graph.<br><br>Explain and run closeness centrality graph algos in Scala                                                                  |
| 10   | Scala domain modeling and modules<br><br>Translate betweenness centrality and PageRank from Python into Scala                         | FP Simplified<br>Chapters 100-106<br>*Domain Modeling, FP with Modules*<br><br>`Graph Algos`<br>Chapter 5, part 3<br>pages 92-108 | Explain and run Scala examples for monads from readings.<br><br>Explain and run betweenness centrality graph algos in Scala                                                                                                       |
