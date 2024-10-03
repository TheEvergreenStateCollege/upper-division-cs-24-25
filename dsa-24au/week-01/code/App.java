
/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        SandwichShop ss = new SandwichShop();

        ss.restockBuns(Bun.CIABATTA, 10);
        ss.restockBuns(Bun.GLUTEN_FREE, 10);
        ss.restockBuns(Bun.SESAME_SEED, 10);
        ss.restockPatties(Patty.BEEF, 1);
        ss.restockPatties(Patty.CHICKEN, 2);
        ss.restockPatties(Patty.PLANT, 1);

        ss.orderSandwich(Patty.CHICKEN, Bun.CIABATTA);
        ss.orderSandwich(Patty.BEEF, Bun.SESAME_SEED);
        ss.orderSandwich(Patty.PLANT, Bun.GLUTEN_FREE);
        ss.orderSandwich(Patty.CHICKEN, Bun.GLUTEN_FREE);
        ss.orderSandwich(Patty.BEEF, Bun.CIABATTA);
        ss.orderSandwich(Patty.PLANT, Bun.SESAME_SEED);
        System.out.println(ss.toString());
    }
}
