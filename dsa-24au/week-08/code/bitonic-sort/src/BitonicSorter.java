import java.util.Arrays;
import java.util.Collections;

public class BitonicSorter<T> {

    public static <T extends Comparable<T>> void sort(T[] arr) {
        sort(arr, 0, arr.length, true);
    }

    public static <T extends Comparable<T>> void sort(T[] arr, int start, int count, boolean increasing) {

        if (count > 1) {
            int k = count >> 1; // divide by 2
            // recurse to the left, increasing half of bitonicity
            sort(arr, start, k, true);
            // recurse to the right, decreasing half of bitonicity
            sort(arr, start+k, k, false);

            // crossover comparators once after each sort before merge down
            // for (int l = start; l < start + k; l += 1) {
            //     if (((arr[l].compareTo(arr[start + k - l - 1]) > 0))) {
            //         T tmp = arr[l];
            //         arr[l] = arr[l+k];
            //         arr[l+k] = tmp;
            //     }
            // }

            merge(arr, start, count, increasing);
        }
    }

    public static <T extends Comparable<T>> void merge(T[] arr, int start, int count, boolean increasing) {
        if (count > 1) {
            int k = count >> 1;
            for (int l = start; l < start + k; l += 1) {
                if (((arr[l].compareTo(arr[l+k]) < 0) != increasing)) {
                    T tmp = arr[l];
                    arr[l] = arr[l+k];
                    arr[l+k] = tmp;
                }
            }
            merge(arr, start, k, increasing);
            merge(arr, start+k, k, increasing);
        }
    }
}
