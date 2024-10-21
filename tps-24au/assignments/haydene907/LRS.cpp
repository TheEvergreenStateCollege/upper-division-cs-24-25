#include <iostream>
#include <vector>
using namespace std;

//either get time limit exceeded error or memory error. I do not know a good way to check for repeats in the repeated
//string list without exceeding allotted time

int main(void) {
    string input;
    vector<string> substrings;
    string lrs = "";
    string foundstrings = "";
    cin >> input;
    int len = input.length();
    
    for (int i = 0; i < len; i++)
    {
        for (int j = 1; j <= len; j++)
        {
            if ((i + j) > len)
            {
                break;
            } 
            string candidate = input.substr(i,j);
            if (input.find(candidate) != input.rfind(candidate))
            {
                if (foundstrings.find(candidate) != string::npos)
                {
                    continue;
                } else 
                {
                    substrings.emplace_back(candidate);
                    foundstrings += candidate + ",";
                }
            }
        }
    }

    lrs = substrings[0];
    for (int i = 1; i < substrings.size(); i++)
    {
        int compareval = lrs.compare(substrings[i]);
        if (compareval == 0)
        {
            continue;
        }
        if (substrings[i].length() > lrs.length())
        {
            lrs = substrings[i];
        }
        else if ((compareval > 0) && (substrings[i].length() == lrs.length())) {
            lrs = substrings[i];
        }
    }
    cout << lrs << endl;
    substrings.clear();
    lrs.clear();
    input.clear();
}