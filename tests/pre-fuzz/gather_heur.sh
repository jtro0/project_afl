#! /bin/bash

Help() {
    echo "This script returns clones all the target repos and gathers heuristics for each. The repos must be from magma, to conform with folder structures"
  	echo
   	echo "Syntax: $0 <path/to/targets> <path/to/heuristic_script>"
   	echo "options:"
   	echo "-h --help    	print help messages."
   	echo
}

Fetch_Targets() {
    echo "Cloning targets"
    for TARGET in $path/*; do
        if [ -d "${TARGET}" ]; then
            export TARGET=$TARGET
            $TARGET/fetch.sh
        fi
    done
}

Fetch_Heuristics() {
    echo "Getting heuristics"
    for TARGET in $path/*; do
        if [ -d "${TARGET}" ]; then
            python $heur $TARGET/repo
        fi
    done
}


if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
    Help $0
    exit 1
fi


# if [ $# -ne 3 ]; then
#     Help $0
#     exit 1
# fi

path=$1
heur=$2

Fetch_Targets $path
Fetch_Heuristics $heur
