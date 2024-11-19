//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.

import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class Main {

    // https://www.baeldung.com/java-executor-wait-for-threads
    public static void awaitTerminationAfterShutdown(ExecutorService threadPool) {
        threadPool.shutdown();
        try {
            if (!threadPool.awaitTermination(60, TimeUnit.SECONDS)) {
                threadPool.shutdownNow();
            }
        } catch (InterruptedException ex) {
            threadPool.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
    public static void main(String[] args) {
        //TIP Press <shortcut actionId="ShowIntentionActions"/> with your caret at the highlighted text
        // to see how IntelliJ IDEA suggests fixing it.
        System.out.printf("Hello Bitonic Sorter Demo");

        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(12);
        executor.submit(() -> {
            Thread.sleep(1000);
            System.out.println("Hello from task 1");
            return null;
        });
        executor.submit(() -> {
            Thread.sleep(1000);
            System.out.println("Hello from task 2");
            return null;
        });
        executor.submit(() -> {
            Thread.sleep(1000);
            System.out.println("Hello from task 3");
            return null;
        });

        assert(2 == executor.getPoolSize());
        assert(1 == executor.getQueue().size());

        awaitTerminationAfterShutdown(executor);

        Integer[] numbers = new Integer[16];
        for (int i = 0; i < numbers.length; i += 1) {
            numbers[i] = (int)Math.round(Math.random() * 100);
            System.out.println(numbers[i]);
        }
        BitonicSorter.sort(numbers);

        System.out.println("Sorted");
        for (int i = 0; i < numbers.length; i += 1) {
            System.out.println(numbers[i]);
        }

    }
}