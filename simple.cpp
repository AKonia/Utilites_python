#include <iostream>
#include <queue>
using namespace std;

int main()
{
	queue<int> q;
	for(int i = 0; i < 10; i++) // Это цикл // Злой комментарий
	{ //Комментарий перед скобкой
		for(int j = 0; j < 10; i++)
		{
			cout << "Count i: " << i+1;
			cout << ", j: " << j+1 << endl;
		}	
	}
	return 0;
}

int getSomeValue() const
{
	int value = 3849238;
	return value;
}
