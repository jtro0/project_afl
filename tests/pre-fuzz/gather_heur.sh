#! /bin/bash
set -e

echo "Getting heuristics"
for TARGET in $TARGETS/*; do
    if [ -d "${TARGET}" ]; then
        # python3 $heur $TARGET/repo
        # mkdir -p $TARGET/heuristics
        python3 $HEURISTIC $TARGET/repo > $TARGET/heuristics.txt
    fi
done


# Help() {
#     echo "This script returns clones all the target repos and gathers heuristics for each. The repos must be from magma, to conform with folder structures"
#   	echo
#    	echo "Syntax: $0 <path/to/targets> <path/to/heuristic_script>"
#    	echo "options:"
#    	echo "-h --help    	print help messages."
#    	echo
# }

# Fetch_Heuristics() {
#     echo "Getting heuristics"
#     for TARGET in $path/*; do
#         if [ -d "${TARGET}" ]; then
#             # python3 $heur $TARGET/repo
#             python3 $heur $TARGET/repo > out/heuristics/$(basename $TARGET)
#         fi
#     done
# }

# Build_Targets() {
#     echo "Building targets"
#     for TARGET in $path/*; do
#         if [ -d "${TARGET}" ]; then
#             export TARGET=$TARGET
#             export OUT=$TARGET/out
#             mkdir -p $OUT
#             # cd $TARGET
#             $TARGET/build.sh
#             # cd $old_dir
#         fi
#     done
# }


# if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
#     Help $0
#     exit 1
# fi


# if [ $# -ne 2 ]; then
#     Help $0
#     exit 1
# fi

# path=$1
# heur=$2
# old_dir=$PWD

# Fetch_Targets $path

# # mkdir -p out/heuristics
# # Fetch_Heuristics $heur
# Build_Targets $path
