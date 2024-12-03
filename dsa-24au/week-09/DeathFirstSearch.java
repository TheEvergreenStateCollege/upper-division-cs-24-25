import java.util.*;
import java.io.*;
import java.math.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Player {

    public static class Pair<T> {

        T first;
        T second;

        public Pair(T first, T second) {
            this.first = first;
            this.second = second;
        }
    }

    public final static Pair<Integer> NOT_FOUND_PAIR = new Pair<>(-1, Integer.MIN_VALUE);

    static class Graph {

        // TODO fill in representation here with appropriate fields (data members)

        Graph(int N) {
          // TODO fill in initialization of your representation
        }

        void addUndirectedEdge(int N1, int N2) {
            // TODO add your code here
        }

        void removeUndirectedEdge(int N1, int N2) {
            // TODO add your code here
        }

        List<Integer> getChildren(int N0) {
            // TODO add your code here
        }
    }

    /**
     * Do a depth first search and return a pair of one of the target indices and the d
     * @param edges
     * @param targets
     * @param start
     * @return an edge to cut from first target found
     */
    public static Pair<Integer> dfs(Graph g, List<Integer> targets, int start, int nodeCount) {
        Stack<Integer> backtrack = new Stack<>();
        // Keep track of visited status of each node in a separate array
        // they default to all false
        // For brute force solution, we don't keep track of which target is closest,
        // just visited list so we don't loop infinitely.
        boolean[] visited = new boolean[nodeCount];
        // Best so far is a pair of (ID of closest target node found so far, and distance)
        Pair<Integer> bestSoFar = NOT_FOUND_PAIR;

        backtrack.push(start);
        while (!backtrack.isEmpty()) {
            int current = backtrack.pop();

            // If we've been visited since we've been added to stack
            if (visited[current]) {
                continue;
            }
            // We only mark a node as visited when we pop it off and examine its children
            List<Integer> children = g.getChildren(current);
            visited[current] = true;

            System.err.println("Current " + current);

            for (Integer child : children) {
                if (targets.contains(child)) {
                    return new Pair<>(current, child);
                }
                if (!visited[child]) {
                    backtrack.push(child);
                }
            }
        }
        return bestSoFar;
    }

    public static void main(String args[]) {

        // undirected graph 

        Scanner in = new Scanner(System.in);
        int N = in.nextInt(); // the total number of nodes in the level, including the gateways
        int L = in.nextInt(); // the number of links
        int E = in.nextInt(); // the number of exit gateways

        // Adjacency 
        boolean[][] edges = new boolean[N][N];
        List<Integer> exits = new ArrayList<>();

        Graph g = new Graph(N);
        for (int i = 0; i < L; i++) {
            int N1 = in.nextInt(); // N1 and N2 defines a link between these nodes
            int N2 = in.nextInt();

            //System.err.println(N1 + " " + N2);
            g.addUndirectedEdge(N1, N2);

        }
        for (int i = 0; i < E; i++) {
            int EI = in.nextInt(); // the index of a gateway node
            exits.add(EI);
        }

        int prevSI = -1;

        // PLAN: Do a DFS from the current Bobnet agent to any of the exits
        // Cut the closest edge to Bob

        // game loop
        while (true) {
            int SI = in.nextInt(); // The index of the node on which the Bobnet agent is positioned this turn

            // We can verify whether SI is a valid move based on previous move.
            Pair<Integer> closestExit = dfs(g, exits, SI, N);

            if (closestExit == NOT_FOUND_PAIR) {
                throw new RuntimeException("No exit found");
            }

            // Write an action using System.out.println()
            // To debug: System.err.println("Debug messages...");

            // Iterate over exits doing DFS to find current location of node


            // Example: 0 1 are the indices of the nodes you wish to sever the link between
            System.out.println(closestExit.first + " " + closestExit.second);

            // Sever the link for next time 
            g.removeUndirectedEdge(closestExit.first, closestExit.second);
            
        }
    }
}
