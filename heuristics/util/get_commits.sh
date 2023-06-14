#! /bin/bash

Help() {
	echo "This script returns all the output of the show command, from any commit in a git log."
  	echo
   	echo "Syntax: ./get_commits -p 'path/to/cloned/repo'"
   	echo "options:"
   	echo "-p    		path to the repo."
   	echo "-h --help    	print help messages."
   	echo
}

if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
    Help
    exit 0
fi

path=$2
cd $path
git log --source | grep -E '^commit .*HEAD$' | cut -c8- | rev | cut -c6- | rev | xargs -I {} git --no-pager diff {}
