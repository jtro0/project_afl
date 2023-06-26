#!/bin/bash

if [ $# -ne 4 ]; then
    echo "Usage: $0 <program> <script> <script input file> <script output file>"
    echo "Example: $0 /path/to/program /path/to/script input.json output.json"
    echo "Program is the program to analyse"
    echo "Script is the script to run with Ghidra"
    exit 1
fi
PROGRAM=$1
SCRIPT=$2
INPUT_FILE=$3
OUTPUT_FILE=$4

echo $PROGRAM
echo $SCRIPT
echo $INPUT_FILE
echo $OUTPUT_FILE

mkdir ghidra_scripts/headless
$GHIDRA_ROOT/support/analyzeHeadless ghidra_scripts/headless Scripting -import $PROGRAM -overwrite -postScript $SCRIPT $INPUT_FILE
