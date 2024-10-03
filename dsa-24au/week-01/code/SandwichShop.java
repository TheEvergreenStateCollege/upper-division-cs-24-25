public class SandwichShop {

    public final int MAX_SANDWICHES = 20;

    int[] bunCounts = new int[Bun.values().length];
    int[] pattyCounts = new int[Patty.values().length];

    Sandwich[] sandwiches;
    int current;

    public SandwichShop() {
        sandwiches = new Sandwich[MAX_SANDWICHES];
        current = 0;
    }

    public void restockBuns(Bun bunType, int count) {
        bunCounts[bunType.ordinal()] += count;
    }

    public void restockPatties(Patty pattyType, int count) {
        pattyCounts[pattyType.ordinal()] += count;
    }

    public boolean orderSandwich(Patty patty, Bun bun) {
        if (bunCounts[bun.ordinal()] < 2) {
            return false;
        }
        if (pattyCounts[patty.ordinal()] < 1) {
            return false;
        }
        sandwiches[current] = new Sandwich(patty, bun);
        bunCounts[bun.ordinal()] -= 2;
        pattyCounts[patty.ordinal()] -= 1;
        current += 1;
        return true;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Sandwich s: sandwiches) {
            sb.append(s);
        }
        return sb.toString();
    }

    public Sandwich[] checkout() {
        return sandwiches;
    }

    public int getSandwichCount() {
        return this.current;
    }
}