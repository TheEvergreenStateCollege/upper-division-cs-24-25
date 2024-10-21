#include <iostream>
#include <vector>
using namespace std;

int main(void) {
    string input;
    vector<string> substrings;
    vector<string> repeatedsubs;
    string lrs = "";
    cin >> input;
    
    for (int i = 0; i < input.length(); i++)
    {
        for (int j = 1; j <= input.length(); j++)
        {
            if ((i + j) > input.length())
            {
                break;
            } else 
            {
                substrings.emplace_back(input.substr(i, j));
            }
        }
    }

    for (int i = 0; i < substrings.size(); i++)
    {
        for (int j = i + 1; j < substrings.size(); j++)
        {
            if ((substrings[i].compare(substrings[j]) == 0) && (substrings[i].length() > lrs.length()))
            {
                lrs = substrings[i];
            }
        }
    }
    cout << lrs << endl;
    substrings.clear();
}