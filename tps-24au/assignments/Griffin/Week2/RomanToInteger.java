class Solution {
    public int romanToInt(String s) {
        HashMap<Character, Integer> romanValues = new HashMap<>();

        int sum = 0;

        romanValues.put('V', 5);
        romanValues.put('L', 50);
        romanValues.put('D', 500);
        romanValues.put('M', 1000);
        
        //loop through string
        for (int i = 0; i < s.length(); ++i) {
            //for each character:
            char index = s.charAt(i);
            
            switch(index) {
                //
                case 'V':
                    sum += 5;
                    break;
                
                case 'L':
                    sum += 50;
                    break;

                case 'D':
                    sum += 500;
                    break;

                case 'M':
                    sum += 1000;
                    break;

                //subtraction pairs
                case 'I':
                    System.out.print("I");
                    if (i + 1 < s.length()) {
                        char nextChar = s.charAt(i + 1);

                        switch(nextChar) {
                            case 'V':
                                System.out.print('V');
                                sum += 4;
                                i += 1;
                                break;

                            case 'X':
                                System.out.print('X');
                                sum += 9;
                                i += 1;
                                break;

                            default:
                                sum += 1;
                                break;
                        }
                    } else {
                        sum += 1;
                    }

                    
                    break;
                
                case 'X':
                    if (i + 1 < s.length()) {
                        char nextChar = s.charAt(i + 1);

                        switch(nextChar) {
                            case 'L':
                                sum += 40;
                                i += 1;
                                break;

                            case 'C':
                                sum += 90;
                                i += 1;
                                break;

                            default:
                                sum += 10;
                                break;
                        }
                    }
                    else {
                        sum += 10;
                    }
                    System.out.print("X");
                    break;
                
                case 'C':
                    if (i + 1 < s.length()) {
                        char nextChar = s.charAt(i + 1);

                        switch(nextChar) {
                            case 'D':
                                sum += 400;
                                i += 1;
                                break;
                            
                            case 'M':
                                sum += 900;
                                i += 1;
                                break;

                            default:
                                sum += 100;
                                break;
                        }
                    }
                    else {
                        sum += 100;
                    }
                    System.out.print("C");
                    break;

            }
        }
        return sum;
    }
}