#!/bin/bash

if [ $# -ne 5 ]; then
    echo "Usage: $0 <program> <script> <script input file> <script output file> <max depth for function calls>"
    echo "Example: $0 /path/to/program /path/to/script input.json output.json"
    echo "Program is the program to analyse"
    echo "Script is the script to run with Ghidra"
    exit 1
fi
PROGRAM=$1
SCRIPT=$2
INPUT_FILE=$3
OUTPUT_FILE=$4
MAX_DEPTH=$5

echo $PROGRAM
echo $SCRIPT
echo $INPUT_FILE
echo $OUTPUT_FILE

mkdir ghidra_scripts/headless
$GHIDRA_ROOT/support/analyzeHeadless $GHIDRA_WORKDIR Scripting -import $PROGRAM -overwrite -postScript $SCRIPT $INPUT_FILE $OUTPUT_FILE $MAX_DEPTH
