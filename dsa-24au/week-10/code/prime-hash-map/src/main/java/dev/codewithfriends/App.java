package dev.codewithfriends;

import java.util.Map;
import java.util.stream.IntStream;
import java.util.Random;

public class App 
{

    final static int COUNT = 10_000_000;

    public static void main( String[] args )
    {
        Map<Integer,Integer> map = new HashMapWrapper<Integer,Integer>(COUNT / 100, COUNT);
	Random rand = new Random();

	IntStream stream = IntStream.range(1, COUNT);
	
	long start = System.currentTimeMillis();
	stream.forEach(i -> map.put(rand.nextInt(COUNT), i));
	System.out.println("All the puts Elapsed " + (System.currentTimeMillis() - start));

	IntStream stream2 = IntStream.range(1, COUNT);
	start = System.currentTimeMillis();
	stream2.forEach(i -> map.get(i));
	System.out.println("All the gets Elapsed " + (System.currentTimeMillis() - start));
	
    }
}
