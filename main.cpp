#include <iostream>
#include <cstdlib>
#include <map>
#include <string>
using std::cout, std::map;

int main(int argc, char** argv)
{
	struct 
	{
		int prot;
		char* host;
		unsigned short port = 25565;
		int state = 1;
	} h;
	
	if (argc > 2)
	{
		h.host = argv[1];
		if (argc > 3)
		{
			h.port = atoi(argv[2]);
		}
	} else 
	{
		cout << "Usage: ./mcping (host) [port]\n";
	}
}
