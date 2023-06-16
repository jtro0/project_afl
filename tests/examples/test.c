#include <stdio.h>
#include <string.h>

void handle_key_secret(char *key) {
	printf("SECRET KEY DETECTED: %s\n", key);
}

void handle_key(char *key) {
	printf("The key is %s\n", key);
}

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("Invalid usage: %s <key>\n", argv[0]);
		return 1;
	}

	int secret = 0;

	char *key=NULL;

	if (strncmp(argv[1], "ABCD", 4) == 0) {
		puts("KEY ACCEPTED");
		key = &(argv[1][4]);
	} else if (strncmp(argv[1], "SECRET", 6) == 0) {
		puts("HOW DID YOU FIND THIS??");
		secret=1;
		key = &(argv[1][6]);
	} else {
		puts("INVALID KEY");
		return 1;
	}

	if (secret) {
		handle_key_secret(key);
	} else {
		handle_key(key);
		puts("fuck it we handle the secret anyway but a secret secret");

		handle_key_secret("NOT THE REAL SECRET");
	}

	return 0;
}