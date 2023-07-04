# #!/bin/bash
# set -e

# ##
# # Pre-requirements:
# # - env FUZZER: path to fuzzer work dir
# # - env TARGET: path to target work dir
# # - env MAGMA: path to Magma support files
# # - env OUT: path to directory where artifacts are stored
# # - env CFLAGS and CXXFLAGS must be set to link against Magma instrumentation
# ##

# export CC="$FUZZER/repo/afl-clang-fast"
# export CXX="$FUZZER/repo/afl-clang-fast++"
# export AS="llvm-as"
# export RANLIB=llvm-ranlib 
# export AR=llvm-ar

# export LIBS="$LIBS -lc++ -lc++abi $FUZZER/repo/utils/aflpp_driver/libAFLDriver.a"

# # AFL++'s driver is compiled against libc++
# export CXXFLAGS="$CXXFLAGS -stdlib=libc++"

# python3 $FUZZER/repo_temp/heuristics/heuristic_diff.py $TARGET/repo -H 0 > $TARGET/heuristics.txt
# cat $TARGET/heuristics.txt

# mkdir -p $FUZZER/headless

# # Build the AFL-only instrumented version
# (
#     export OUT="$OUT/afl"
#     export LDFLAGS="$LDFLAGS -L$OUT"

#     # "$MAGMA/build.sh"
#     # export LDFLAGS="$LDFLAGS -O1 -static"

#     "$TARGET/build.sh"
#     export DATA_PATH=$TARGET/heuristics.txt
#     for PROG in $OUT/*; do
#         if [ -x $PROG ]
#         then
#             export PROG=$PROG
#             # $FUZZER/ghidra/ghidra_10.3.1_PUBLIC/support/analyzeHeadless $FUZZER/headless Scripting -import $PROG -overwrite -scriptPath $FUZZER/repo_temp/ghidra_scripts -postScript get_bitmap_offsets.py 
            
#             export GHIDRA_ROOT=$FUZZER/ghidra/ghidra_10.3.1_PUBLIC 
#             sh $FUZZER/repo_temp/ghidra_scripts/run_headless.sh $PROG $FUZZER/repo_temp/ghidra_scripts/get_bitmap_offsets.py $TARGET/heuristics.txt $TARGET/output.txt 10
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

#     # "$MAGMA/build.sh"
#     # export LDFLAGS="$LDFLAGS -O1 -static"

#     "$TARGET/build.sh"
#     export DATA_PATH=$TARGET/heuristics.txt

#     for PROG in $OUT/*; do
#         if [ -x $PROG ]
#         then
#             export PROG=$PROG
#             # $FUZZER/ghidra/ghidra_10.3.1_PUBLIC/support/analyzeHeadless $FUZZER/headless Scripting -import $PROG -overwrite -scriptPath $FUZZER/repo_temp/ghidra_scripts -postScript get_bitmap_offsets.py $TARGET/heuristics.txt
#             export GHIDRA_ROOT=$FUZZER/ghidra/ghidra_10.3.1_PUBLIC 
#             sh $FUZZER/repo_temp/ghidra_scripts/run_headless.sh $PROG $FUZZER/repo_temp/ghidra_scripts/get_bitmap_offsets.py $TARGET/heuristics.txt $TARGET/output.txt 10
#         else
#             echo "Not executable"
#         fi
#     done
# )



# ls $FUZZER/ghidra
# export GHIDRA_ROOT=$FUZZER/ghidra


# NOTE: We pass $OUT directly to the target build.sh script, since the artifact
#       itself is the fuzz target. In the case of Angora, we might need to
#       replace $OUT by $OUT/fast and $OUT/track, for instance.


#!/bin/bash
set -e

##
# Pre-requirements:
# - env FUZZER: path to fuzzer work dir
# - env TARGET: path to target work dir
# - env MAGMA: path to Magma support files
# - env OUT: path to directory where artifacts are stored
# - env CFLAGS and CXXFLAGS must be set to link against Magma instrumentation
##

export CC="$FUZZER/repo/afl-clang-lto"
export CXX="$FUZZER/repo/afl-clang-lto++"
LLVM_PATH=/usr/lib/llvm-11/bin
export AS="${LLVM_PATH}/llvm-as"
export RANLIB="${LLVM_PATH}/llvm-ranlib"
export AR="${LLVM_PATH}/llvm-ar"
export LD="${LLVM_PATH}/ld.lld"
export NM="${LLVM_PATH}/llvm-nm"

export LIBS="$LIBS -lstdc++ $FUZZER/repo/utils/aflpp_driver/libAFLDriver.a"

# Some targets do not support a static AFL memory region
# DYNAMIC_TARGETS=(php openssl)
# TARGET_NAME="$(basename $TARGET)"
# if [[ " ${DYNAMIC_TARGETS[@]} " =~ " $TARGET_NAME " ]]; then
#     export AFL_LLVM_MAP_DYNAMIC=1
# fi

export PST_OUT=$OUT/pst
mkdir -p $PST_OUT

python3 $FUZZER/repo_temp/heuristics/heuristic_diff.py $TARGET/repo -H 0 > $PST_OUT/heuristics.txt
cat $PST_OUT/heuristics.txt

export GHIDRA_WORKDIR=$FUZZER/headless
mkdir -p $GHIDRA_WORKDIR

export CONFIG_FLAGS="--disable-shared"

# Build the AFL-only instrumented version
(
    export OUT="$OUT/afl"
    export LDFLAGS="$LDFLAGS -L$OUT"

    "$MAGMA/build.sh"
    # export LDFLAGS="$LDFLAGS -O1 -static"
    "$TARGET/build.sh"

    export DATA_PATH=$TARGET/heuristics.txt
    for PROG in $OUT/*; do
        if [ -x $PROG ]
        then
            export PROG=$PROG
            # $FUZZER/ghidra/ghidra_10.3.1_PUBLIC/support/analyzeHeadless $FUZZER/headless Scripting -import $PROG -overwrite -scriptPath $FUZZER/repo_temp/ghidra_scripts -postScript get_bitmap_offsets.py 
            
            export GHIDRA_ROOT=$FUZZER/ghidra/ghidra_10.3.1_PUBLIC 
            sh $FUZZER/repo_temp/ghidra_scripts/run_headless.sh $PROG $FUZZER/repo_temp/ghidra_scripts/get_bitmap_offsets.py $PST_OUT/heuristics.txt $PST_OUT/output_bitmap 10
        else
            echo "Not executable"
        fi
    done
)

# Build the CmpLog instrumented version

(
    export OUT="$OUT/cmplog"
    export LDFLAGS="$LDFLAGS -L$OUT"

    export AFL_LLVM_CMPLOG=1

    "$MAGMA/build.sh"
    export LDFLAGS="$LDFLAGS -static"
    "$TARGET/build.sh"

    export DATA_PATH=$TARGET/heuristics.txt
    for PROG in $OUT/*; do
        if [ -x $PROG ]
        then
            export PROG=$PROG
            # $FUZZER/ghidra/ghidra_10.3.1_PUBLIC/support/analyzeHeadless $FUZZER/headless Scripting -import $PROG -overwrite -scriptPath $FUZZER/repo_temp/ghidra_scripts -postScript get_bitmap_offsets.py 
            
            # export GHIDRA_ROOT=$FUZZER/ghidra/ghidra_10.3.1_PUBLIC 
            # sh $FUZZER/repo_temp/ghidra_scripts/run_headless.sh $PROG $FUZZER/repo_temp/ghidra_scripts/get_bitmap_offsets.py $PST_OUT/heuristics.txt $PST_OUT/output_bitmap 10
        else
            echo "Not executable"
        fi
    done
)

# NOTE: We pass $OUT directly to the target build.sh script, since the artifact
#       itself is the fuzz target. In the case of Angora, we might need to
#       replace $OUT by $OUT/fast and $OUT/track, for instance.
