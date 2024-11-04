import java.util.ArrayList;

class Solution {
    ArrayList<Double> powersOfTwo = new ArrayList<Double>();
    ArrayList<Boolean> reverseBinaryComplement = new ArrayList<Boolean>();

    ArrayList<Boolean> getBinaryComplement(int num) {
        ArrayList<Boolean> binaryString = new ArrayList<Boolean>();
        //find highest bit
        boolean firstBitFound = false;

        for (int i = powersOfTwo.size() - 1; i > -1; --i) {
            if (num - powersOfTwo.get(i) > -1) {
                firstBitFound = true;
                binaryString.add(false);
                num -= powersOfTwo.get(i).doubleValue();
                //System.out.println(0);
            }
            else if (firstBitFound) {
                binaryString.add(true); 
                //System.out.println(1);
            }
        }
        return binaryString;
    }

    //entry
    public int findComplement(int num) {
        int complement = 0;

        //calculate powers of 2. Not lazy
        for (int i = 0; i < 31; ++i) {
            powersOfTwo.add(Math.pow(2, i));
            //System.out.println(Math.pow(2, i));
        }

        //get binary string
        ArrayList<Boolean> binaryComplement = getBinaryComplement(num);
        
        //reverse binary string -- so it can be easily compared to powers of 2
        for (int i = binaryComplement.size() - 1; i > -1; --i) {
            reverseBinaryComplement.add(binaryComplement.get(i));
        }

        //loop through reverse binary complement, if TRUE: complement += powersOfTwo(i)
        for (int i = 0; i < reverseBinaryComplement.size(); ++i) {
            if (reverseBinaryComplement.get(i)) {
                complement += powersOfTwo.get(i);
            }
        }
        

    return complement;
    }
}