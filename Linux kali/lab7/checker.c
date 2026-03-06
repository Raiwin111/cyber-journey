#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
	//check was the password sent?
	if (argc < 2) return 1;

	char *secret ="kali123"; // password is correct
	
	if(strcmp(argv[1], secret) ==0){
		printf("SUCCESS");
}	else {
		printf("FAILED");
}	return 0;
}
