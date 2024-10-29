#include <iostream>
#include <vector>
using namespace std;

//either get time limit exceeded error or memory error. I do not know a good way to check for repeats in the repeated
//string list without exceeding allotted time

int main(void) {
    string input;
    string lrs = "";
    cin >> input;
    int len = input.length();
    
    for (int i = 0; i < len; i++)
    {
        string candidate = "";
        int iterator = i;
        for (int j = 1; j <= len; j++)
        {
            if (input[iterator] == input[j]){
                candidate += input[j];
                iterator++;
            } else {
                if (candidate.length() > lrs.length()){
                    lrs = candidate;
                } else if ((candidate.length() == lrs.length()) && (lrs.compare(candidate) > 0)) {
                    lrs = candidate;
                }
                iterator = i;
                candidate = "";
            }
        }
    }
    cout << lrs << endl;
    lrs.clear();
    input.clear();
}