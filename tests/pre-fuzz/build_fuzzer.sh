#!/bin/bash
set -e

OLD_DIR=$PWD
# Preinstall
apt-get update && \
    apt-get install -y make clang-15 llvm-15-dev libc++-15-dev libc++abi-15-dev \
        build-essential git wget gcc-12-plugin-dev

update-alternatives \
  --install /usr/lib/llvm              llvm             /usr/lib/llvm-15  20 \
  --slave   /usr/bin/llvm-config       llvm-config      /usr/bin/llvm-config-15  \
    --slave   /usr/bin/llvm-ar           llvm-ar          /usr/bin/llvm-ar-15 \
    --slave   /usr/bin/llvm-as           llvm-as          /usr/bin/llvm-as-15 \
    --slave   /usr/bin/llvm-bcanalyzer   llvm-bcanalyzer  /usr/bin/llvm-bcanalyzer-15 \
    --slave   /usr/bin/llvm-c-test       llvm-c-test      /usr/bin/llvm-c-test-15 \
    --slave   /usr/bin/llvm-cov          llvm-cov         /usr/bin/llvm-cov-15 \
    --slave   /usr/bin/llvm-diff         llvm-diff        /usr/bin/llvm-diff-15 \
    --slave   /usr/bin/llvm-dis          llvm-dis         /usr/bin/llvm-dis-15 \
    --slave   /usr/bin/llvm-dwarfdump    llvm-dwarfdump   /usr/bin/llvm-dwarfdump-15 \
    --slave   /usr/bin/llvm-extract      llvm-extract     /usr/bin/llvm-extract-15 \
    --slave   /usr/bin/llvm-link         llvm-link        /usr/bin/llvm-link-15 \
    --slave   /usr/bin/llvm-mc           llvm-mc          /usr/bin/llvm-mc-15 \
    --slave   /usr/bin/llvm-nm           llvm-nm          /usr/bin/llvm-nm-15 \
    --slave   /usr/bin/llvm-objdump      llvm-objdump     /usr/bin/llvm-objdump-15 \
    --slave   /usr/bin/llvm-ranlib       llvm-ranlib      /usr/bin/llvm-ranlib-15 \
    --slave   /usr/bin/llvm-readobj      llvm-readobj     /usr/bin/llvm-readobj-15 \
    --slave   /usr/bin/llvm-rtdyld       llvm-rtdyld      /usr/bin/llvm-rtdyld-15 \
    --slave   /usr/bin/llvm-size         llvm-size        /usr/bin/llvm-size-15 \
    --slave   /usr/bin/llvm-stress       llvm-stress      /usr/bin/llvm-stress-15 \
    --slave   /usr/bin/llvm-symbolizer   llvm-symbolizer  /usr/bin/llvm-symbolizer-15 \
    --slave   /usr/bin/llvm-tblgen       llvm-tblgen      /usr/bin/llvm-tblgen-15

update-alternatives \
  --install /usr/bin/clang                 clang                  /usr/bin/clang-15     20 \
  --slave   /usr/bin/clang++               clang++                /usr/bin/clang++-15 \
  --slave   /usr/bin/clang-cpp             clang-cpp              /usr/bin/clang-cpp-15

apt-get update && \
    apt-get install -y unzip openjdk-17-jdk-headless

# Build fuzzer
if [ ! -d "$FUZZER" ]; then
    echo "Fuzzer folder does not exist"
    exit 1
fi

cd "$FUZZER"
export CC=clang
export CXX=clang++
# export AFL_NO_X86=1
export PYTHON_INCLUDE=/
make -j$(nproc) || exit 1
make -C utils/aflpp_driver || exit 1

mkdir -p "$OUT/afl" "$OUT/cmplog"
cd $OLD_DIR

