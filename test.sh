#!/bin/bash
PROG=$1

if [ -x $PROG ]
then
	echo "exec"
else
	echo "not exec"
fi
