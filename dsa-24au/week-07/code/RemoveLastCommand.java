import java.util.ArrayList;

public class RemoveLastCommand extends UndoCommand {
   private ArrayList<String> sourceList;

   public RemoveLastCommand(ArrayList<String> list) {
      this.sourceList = list;
   }

   @Override
   public void execute() {
      // TODO: Type your code here
   }
}
