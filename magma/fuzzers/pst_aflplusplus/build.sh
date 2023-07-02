#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
##

# if [ ! -d "$FUZZER/repo" ]; then
#     echo "fetch.sh must be executed first."
#     exit 1
# fi

# cd "$FUZZER/repo"
# export CC=clang
# export CXX=clang++
# export AFL_NO_X86=1
# export PYTHON_INCLUDE=/
# make -j$(nproc) || exit 1
# make -C utils/aflpp_driver || exit 1

# mkdir -p "$OUT/afl" "$OUT/cmplog"


# Build fuzzer
if [ ! -d "$FUZZER" ]; then
    echo "Fuzzer folder does not exist"
    echo $FUZZER
    exit 1
fi

export REAL_CC=gcc 
export REAL_CXX=g++
export LLVM_CONFIG=llvm-config-11

cd "$FUZZER/repo"
make -j$(nproc) all || exit 1
make -C utils/aflpp_driver || exit 1

mkdir -p "$OUT/afl" "$OUT/cmplog"
# cd $OLD_DIR

