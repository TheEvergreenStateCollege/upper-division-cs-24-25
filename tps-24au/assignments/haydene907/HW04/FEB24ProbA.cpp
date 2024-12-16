//Feb 2024 PNW Programming Contest Div 1 Problem A:
//Hayden Edge
#include <vector>
#include <cstring>
using namespace std;

bool char_needed(char c, char* needed_chars)
{
	bool needed = false;
	for (int i = 0; i < 3; i++)
	{
		needed = (needed_chars[i] == c) ? true : needed;
	}
	return needed;
}



int main()
{
	string input;
	cin >> input;
	vector<string*> subsequences;
	subsequences.push_back(&input);

	if (input.length() % 3 == 0)
	{
		for (int i = 0; i < subsequences.size(); i++)
		{
			char needed_chars[] = "ABC";
			bool afound, bfound, cfound = false;
			for (int j = 0; j < input.length(); j++)
			{
				if (char_needed(subsequences[i]->at(j), &needed_chars))
				{
					
				}
			}
		}
	}
}