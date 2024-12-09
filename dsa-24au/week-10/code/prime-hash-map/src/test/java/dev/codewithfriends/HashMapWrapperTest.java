package dev.codewithfriends;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class HashMapWrapperTest {
    @Test
    public void getAndPutTest() {
        HashMapWrapper<String, String> hm = new HashMapWrapper<String, String>(3, 20);

        String result = hm.put("Hello", "World");
        assertEquals(result, "World");
        hm.put("PaulBlart", "MallCop");

        assertEquals(hm.get("Hello"), "World");
        assertEquals(hm.get("PaulBlart"), "MallCop");
    }
}
