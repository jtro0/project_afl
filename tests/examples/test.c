#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void handle_key_secret(char *key) {
	printf("SECRET KEY DETECTED: %s\n", key);
}

void handle_key(char *key) {
	printf("The key is %s\n", key);
}

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("Invalid usage: %s <key_file>\n", argv[0]);
		return 1;
	}

	FILE *fp = fopen(argv[1], "r");

	if (fp == NULL) {
		printf("Couldnt open '%s'\n", argv[1]);
		return 1;
	}

	fseek(fp, 0, SEEK_END);
	size_t size = ftell(fp);
	fseek(fp, 0, SEEK_SET);

	char *input_data = calloc(1, size);

	fread(input_data, size, 1, fp);

	int secret = 0;

	char *key=NULL;

	if (strncmp(input_data, "ABCD", 4) == 0) {
		puts("KEY ACCEPTED");
		key = &(input_data[4]);
	} else if (strncmp(input_data, "SECRET", 6) == 0) {
		puts("HOW DID YOU FIND THIS??");
		secret=1;
		key = &(input_data[6]);
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