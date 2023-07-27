# **P**roject **S**ystem **T**esting Fuzzer
A directed fuzzer based on [AFLplusplus](https://github.com/AFLplusplus/AFLplusplus) making use of git commits to target most frequently, or recently, updated functions.

# How to run
## With Magma
[Magma](https://hexhive.epfl.ch/magma/) can be used to run this fuzzer. 
It has been included in this repo, but can also be cloned as usual. 
The build scripts need to be copied to make it work. 
These can be found in [magma/fuzzers/pst_aflplusplus(_recent_commit)](magma/fuzzers).

To run with magma, simply execute the [run.sh](magma/tools/captain/run.sh).

## Bare
Follow the instructions [here](https://github.com/AFLplusplus/AFLplusplus/blob/stable/docs/INSTALL.md) on how to build regular AFLplusplus.
Also instrument your target binary, build your target according to their instructions.

Before running, we need to gather heuristic information and find where the functions are in the bitmap.

First, run `python3 heuristics/heuristic_diff.py $TARGET -H 0`.
Set the environment variable `TARGET` to the git repo of the target.
Also this script accepts `-H 0` and `-H 1`, the former option is most frequently updated functions, the latter is most recently updated. 
See `python3 heuristics/heuristic_diff.py` for help. 
Save this file, somewhere like `$OUT/heuristics.txt`.

Next, analyse the instrumented binary with our Ghidra script.
Download and install Ghida, and its dependencies from their github: [Ghidra](https://github.com/NationalSecurityAgency/ghidra).
Run our headless script as follows: `sh ghidra_scripts/run_headless.sh $PROG ghidra_scripts/get_bitmap_offsets.py $OUT/heuristics.txt $OUT/output_bitmap 10`
Before running this, be sure to set the set environment variables `$GHIDRA_ROOT`, root folder of your Ghidra installation, `$PROG`, the instrumented binary needed to analyse, and `$OUT` which is the output folder.
The last variable can be set to any integer, and represents the max-depth the script takes which recursively searching.
This will write to file `$OUT/output_bitmap` which we will need for fuzzing.

Lastly, fuzz!
The following command will run AFLplusplus with our weights:
```
afl-fuzz -i input -o output $FUZZARGS -j $OUT/output_bitmap -- $PROG $ARGS
```
It is crucial to give argument `-j` to run with our fuzzer, otherwise it is default aflplusplus.
For more information on how to run AFLplusplus, read [their documentation](https://github.com/AFLplusplus/AFLplusplus/blob/stable/docs/fuzzing_in_depth.md)

# Results and report
Magma even comes with data collecting and self reporting scripts.
These scripts are found in [magma/tools/report_df](magma/tools/report_df).
To read more on how to use these, refer to the [magma documentations](https://hexhive.epfl.ch/magma/docs/technical.html#exp2jsonpy).

Our generated report can be found [here](magma/tools/report_df/long_data/index.md), definetly check it out!

# Troubleshoot
## It is stuck at `RUN /magma/fuzzers/afl_asan/instrument.sh`
It is not stuck, it just takes a really long time sometimes (more than 5 hours at times). 
Do not worry, if you have done this once you can reuse the docker image and cache. 
It is only needed once.

## core_pattern
It can be that the fuzzer encounters a warning message to enable core_pattern.
To do so execute the following as root:
```
#  echo core > /proc/sys/kernel/core_pattern
```
