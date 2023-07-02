set -e

echo "Please set FUZZER, MAGMA, and GHIDRA to the corresponding root folders."

# export FUZZER=../AFLplusplus
# export OUT=temp
if [ ! -d $OUT ]
then mkdir -p $OUT
fi

export TARGETS=$MAGMA/targets

sh pre-fuzz/build_fuzzer.sh

sh pre-fuzz/gather_targets.sh

export TARGETS=$OUT/targets
export HEURISTIC=../heuristics/heuristic_diff.py
sh pre-fuzz/gather_heur.sh

export TARGET=$TARGETS/libpng
export OUT=$TARGET/out
echo $OUT
mkdir -p $OUT
sh pre-fuzz/instrument.sh

# export DATA_PATH= $TARGET/heuristics.txt
# export PROG=$(basename $TARGET)
# $GHIDRA/support/analyzeHeadless $GHIDRA_WORKDIR/headless Scripting -import $TARGET/out/afl/libpng_read_fuzzer -overwrite -scriptPath $GHIDRA_WORKDIR -postScript get_bitmap_offsets.py