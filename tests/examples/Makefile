CC=cc
# AFL_CC=afl-cc
AFL_CC=afl-clang-lto
DEPS=test.c
CFLAGS=-I. -O0
LIBS=-lm

all: $(DEPS)
		$(AFL_CC) -o test $(CFLAGS) $^ $(LIBS)

cov: $(DEPS)
		$(CC) -o test_cov $(CFLAGS) -fprofile-arcs -ftest-coverage $^ $(LIBS)

.PHONY: clean

clean:
		rm ./test ./test_cov