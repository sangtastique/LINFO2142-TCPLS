#!/usr/bin/env sh

# Get absolute path
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH


cp $SCRIPTPATH/rapido-edit.c $SCRIPTPATH/../deps/rapido/t/rapido.c
# # Navigate to rapido folder containing rapido's repo
cd $SCRIPTPATH/../deps/rapido

# # Build rapido
git submodule update --init
cmake .
make rapido
# # Move the binary in our repo :)
cp rapido $SCRIPTPATH/rapido-edit
