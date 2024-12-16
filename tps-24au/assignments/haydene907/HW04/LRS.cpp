/*Written by Hayden Edge, 12/9/2024*/

#include <iostream>
#include <vector>
using namespace std;

class SuffixTree 
{
private:
	class node 
	{
	public:
		char value;
		vector<node*> children;
		node* parent;
		bool isHead;
		int insertcount;
		node(char val, node* par, bool head)
		{
			value = val;
			parent = par;
			isHead = head;
			insertcount = 1;
		} 
	};
	string lrs;
	node* head;

public:
	SuffixTree() 
	{
		head = new node('\0', nullptr, true);
	}
	//Inserts string character by character into suffix tree and counts number of times
	//it didnt need to create a child node, then returns it. This indicates how much of
	//the substring was already within the tree and therefore duplicates.
	int insert(string *ptr)
	{
		node* examined = head;
		int num_matched = 0;
		for (int i = 0; i < ptr->length(); i++)
		{
			bool match = false;
			for (int j = 0; j < examined->children.size(); j++)
			{
				if (examined->children[j]->value == ptr->at(i)) 
				{
					match = true;
					examined = examined->children[j];
					examined->insertcount++;
					num_matched++;
					break;
				}
			}
			if (match != true)
			{
				examined->children.push_back(new node(ptr->at(i), examined, false));
				examined = examined->children[examined->children.size() - 1];
			}
		}
		return num_matched;
	}

};



//TODO: to improve insertion time, possible implement Ukonnens.
//Currently Insertion and substring detection together are O(n^2).

//But using Ukonnens Algo Insertion could be O(n) and then a faster than O(n)
//traversal to detect repeats, maybe DFS for nodes with more than one child?


int main(void) {
	string input;
    string lrs = "";
    cin >> input;
    SuffixTree tree;

    for (int i = 0; i < input.length(); i++)
    {
    	string substr = input.substr(i, string::npos);
    	int matches = tree.insert(&substr);
    	substr = input.substr(i,matches);
    	lrs = (matches > lrs.length()) ? substr : lrs;
    	lrs = ((matches == lrs.length()) && (lrs.compare(substr) > 0)) ? substr : lrs;
    	//probably not as efficient here with 2 ternary's but I cant stand to see another
    	//if statement block.
    }
    cout << lrs << endl;
}