#!/bin/bash
set -e

# Instrument
export CC="$FUZZER/afl-clang-lto"
export CXX="$FUZZER/afl-clang-lto++"
export AS="llvm-as"

# export LIBS="$LIBS -lc++ -lc++abi $FUZZER/utils/aflpp_driver/libAFLDriver.a"
export LIBS="$LIBS -lc++ $FUZZER/utils/aflpp_driver/libAFLDriver.a"

# AFL++'s driver is compiled against libc++
export CXXFLAGS="$CXXFLAGS -stdlib=libc++"

# python3 $FUZZER//heuristics/heuristic_diff.py $TARGET/repo > $TARGET/heuristics.txt
# cat $TARGET/heuristics.txt

export OUT="$OUT/afl"
export LDFLAGS="$LDFLAGS -L$OUT"

mkdir -p $OUT
# "$MAGMA/build.sh"
sh $TARGET/build.sh

# mkdir -p $FUZZER/headless

# # Build the AFL-only instrumented version
# (
#     export OUT="$OUT/afl"
#     export LDFLAGS="$LDFLAGS -L$OUT"

#     "$MAGMA/build.sh"
#     "$TARGET/build.sh"
#     export DATA_PATH=$TARGET/heuristics.txt
#     for PROG in $OUT/*; do
#         if [ -x $PROG ]
#         then
#             export PROG=$PROG
#             $FUZZER/ghidra/ghidra_10.3.1_PUBLIC/support/analyzeHeadless $FUZZER/headless Scripting -import $PROG -overwrite -scriptPath $FUZZER/repo_temp/ghidra_scripts -postScript get_bitmap_offsets.py 
#         else
#             echo "Not executable"
#         fi
#     done
# )

# # Build the CmpLog instrumented version

# (
#     export OUT="$OUT/cmplog"
#     export LDFLAGS="$LDFLAGS -L$OUT"
#     # export CFLAGS="$CFLAGS -DMAGMA_DISABLE_CANARIES"

#     export AFL_LLVM_CMPLOG=1

#     "$MAGMA/build.sh"
#     "$TARGET/build.sh"
#     export DATA_PATH=$TARGET/heuristics.txt

#     for PROG in $OUT/*; do
#         if [ -x $PROG ]
#         then
#             export PROG=$PROG
#             $FUZZER/ghidra/ghidra_10.3.1_PUBLIC/support/analyzeHeadless $FUZZER/headless Scripting -import $PROG -overwrite -scriptPath $FUZZER/repo_temp/ghidra_scripts -postScript get_bitmap_offsets.py $TARGET/heuristics.txt
#         else
#             echo "Not executable"
#         fi
#     done
# )
