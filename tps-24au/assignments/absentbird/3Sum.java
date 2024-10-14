class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> output = new ArrayList<List<Integer>>();
        if (nums.length == 3) {
            if (nums[0] + nums[1] + nums[2] == 0) {
                output.add(new ArrayList<Integer>(Arrays.asList(nums[0], nums[1], nums[2])));
            }
            return output;
        }
        Arrays.sort(nums);
        Set<List<Integer>> answers = new HashSet<List<Integer>>();
        HashMap<Integer, Integer> values = new HashMap();
        for (int i = 0; i < nums.length; i++) {
            if (values.get(nums[i]) == null) {
                values.put(nums[i], i);
            }
        }
        int last = nums[nums.length-1];
        int zeroes = 0;
        for (int i=0; i < nums.length; i++) {
            if (nums[i] > 0) {
                break;
            }
            if (nums[i] == 0) {
                zeroes++;
                continue;
            }
            if (nums[i] == last) {
                continue;
            }
            if (nums[i] + nums[nums.length-1] + nums[nums.length-2] < 0) {
                continue;
            }
            for (int j = nums.length-1; j > i+1; j--) {
                if (nums[i] + nums[i+1] + nums[j] > 0) {
                    continue;
                }
                int gap = (nums[i] + nums[j]) * -1;
                if (values.containsKey(gap) && values.get(gap) < j) {
                    answers.add(new ArrayList<Integer>(Arrays.asList(nums[i], gap, nums[j])));
                }
            }
            last = nums[i];
        }
        if (zeroes > 2) {
            answers.add(new ArrayList<Integer>(Arrays.asList(0,0,0)));
        }
        output.addAll(answers);
        return output;
    }
}

