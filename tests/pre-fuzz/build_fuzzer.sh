#!/bin/bash
set -e

OLD_DIR=$PWD
# Preinstall
# apt-get update && \
#     apt-get install -y make clang-15 llvm-15-dev libc++-15-dev libc++abi-15-dev \
#         build-essential git wget gcc-12-plugin-dev

# update-alternatives \
#   --install /usr/lib/llvm              llvm             /usr/lib/llvm-15  20 \
#   --slave   /usr/bin/llvm-config       llvm-config      /usr/bin/llvm-config-15  \
#     --slave   /usr/bin/llvm-ar           llvm-ar          /usr/bin/llvm-ar-15 \
#     --slave   /usr/bin/llvm-as           llvm-as          /usr/bin/llvm-as-15 \
#     --slave   /usr/bin/llvm-bcanalyzer   llvm-bcanalyzer  /usr/bin/llvm-bcanalyzer-15 \
#     --slave   /usr/bin/llvm-c-test       llvm-c-test      /usr/bin/llvm-c-test-15 \
#     --slave   /usr/bin/llvm-cov          llvm-cov         /usr/bin/llvm-cov-15 \
#     --slave   /usr/bin/llvm-diff         llvm-diff        /usr/bin/llvm-diff-15 \
#     --slave   /usr/bin/llvm-dis          llvm-dis         /usr/bin/llvm-dis-15 \
#     --slave   /usr/bin/llvm-dwarfdump    llvm-dwarfdump   /usr/bin/llvm-dwarfdump-15 \
#     --slave   /usr/bin/llvm-extract      llvm-extract     /usr/bin/llvm-extract-15 \
#     --slave   /usr/bin/llvm-link         llvm-link        /usr/bin/llvm-link-15 \
#     --slave   /usr/bin/llvm-mc           llvm-mc          /usr/bin/llvm-mc-15 \
#     --slave   /usr/bin/llvm-nm           llvm-nm          /usr/bin/llvm-nm-15 \
#     --slave   /usr/bin/llvm-objdump      llvm-objdump     /usr/bin/llvm-objdump-15 \
#     --slave   /usr/bin/llvm-ranlib       llvm-ranlib      /usr/bin/llvm-ranlib-15 \
#     --slave   /usr/bin/llvm-readobj      llvm-readobj     /usr/bin/llvm-readobj-15 \
#     --slave   /usr/bin/llvm-rtdyld       llvm-rtdyld      /usr/bin/llvm-rtdyld-15 \
#     --slave   /usr/bin/llvm-size         llvm-size        /usr/bin/llvm-size-15 \
#     --slave   /usr/bin/llvm-stress       llvm-stress      /usr/bin/llvm-stress-15 \
#     --slave   /usr/bin/llvm-symbolizer   llvm-symbolizer  /usr/bin/llvm-symbolizer-15 \
#     --slave   /usr/bin/llvm-tblgen       llvm-tblgen      /usr/bin/llvm-tblgen-15

# update-alternatives \
#   --install /usr/bin/clang                 clang                  /usr/bin/clang-15     20 \
#   --slave   /usr/bin/clang++               clang++                /usr/bin/clang++-15 \
#   --slave   /usr/bin/clang-cpp             clang-cpp              /usr/bin/clang-cpp-15

sudo apt-get update
sudo apt-get install -y build-essential python3-dev automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools cargo libgtk-3-dev
# try to install llvm 14 and install the distro default if that fails
sudo apt-get install -y lld-14 llvm-14 llvm-14-dev clang-14 || sudo apt-get install -y lld llvm llvm-dev clang
sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev
sudo apt-get install -y ninja-build # for QEMU mode
# git clone https://github.com/AFLplusplus/AFLplusplus
# cd AFLplusplus
# make distrib
# sudo make install

# sudo apt-get install -y unzip openjdk-17-jdk-headless

# Build fuzzer
if [ ! -d "$FUZZER" ]; then
    echo "Fuzzer folder does not exist"
    echo $FUZZER
    exit 1
fi

export REAL_CC=gcc 
export REAL_CXX=g++
export LLVM_CONFIG=llvm-config-14

cd "$FUZZER"
# make clean
# exports CC=gcc
# export CXX=gcc++
# export AFL_NO_X86=1
# export PYTHON_INCLUDE=/
make -j$(nproc) all || exit 1
# make -C utils/aflpp_driver || exit 1

mkdir -p "$OUT/afl" "$OUT/cmplog"
cd $OLD_DIR

