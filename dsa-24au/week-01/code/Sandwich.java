

public class Sandwich {
    Bun topBun;
    Bun bottomBun;
    Patty patty;

    public Sandwich(Patty patty, Bun buns) {
        this.patty = patty;
        this.topBun = buns;
        this.bottomBun = buns;
        System.out.println("New sandwich: " + this.toString());
    }

    public String toString() {
        return this.topBun.toString() + "-" + this.patty.toString();
    }
}
