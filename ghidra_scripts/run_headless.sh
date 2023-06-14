#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <program> <script>"
    echo "Example: $0 /path/to/program /path/to/script"
    echo "Program is the porgram to analyse"
    echo "Script is the script to run with Ghidra"
    exit 1
fi
PROGRAM=$1
SCRIPT=$2

echo $PROGRAM
echo $SCRIPT

mkdir ghidra_scripts/headless
$GHIDRA_ROOT/support/analyzeHeadless ghidra_scripts/headless Scripting -import $PROGRAM -overwrite -postScript $SCRIPT