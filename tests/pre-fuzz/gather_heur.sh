#! /bin/bash

Help() {
    echo "This script returns clones all the target repos and gathers heuristics for each. The repos must be from magma, to conform with folder structures"
  	echo
   	echo "Syntax: $0 -p 'path/to/targets'"
   	echo "options:"
   	echo "-p    		path to the folder with all targets."
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


if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
    Help $0
    exit 1
fi


if [ $# -ne 2 ]; then
    Help $0
    exit 1
fi

path=$2

Fetch_Targets $path
