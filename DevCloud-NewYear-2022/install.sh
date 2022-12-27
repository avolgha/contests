#!/usr/bin/env bash

SCRIPT="https://github.com/avolgha/contests/blob/dev/DevCloud-NewYear-2022/neujahr.py?raw=true"
LOCATION="/home/$(whoami)/.local/bin"

echo "executing: neujahr.py installer"
echo "info: will install script to '$LOCATION'"
echo "      if you prefer a custom installation, exit now"
echo "      or press ENTER to continue."

read || exit 1

mkdir -p "$LOCATION"

if [ -f "$LOCATION/neujahr.py" ]; then
	echo "skip: already contains an instance of 'neujahr.py'."
	echo "      please remove this instance and run the installer"
	echo "      again if this is an error."
	exit 0
fi

wget -O "$LOCATION/neujahr.py" "$SCRIPT" &>/dev/null

chmod +x "$LOCATION/neujahr.py"

echo "info: please add the following line to your shell"
echo "      entry file to execute the program when you"
echo "      enter your shell:"
echo ""
echo "  neujahr.py run"
echo ""
echo "(if you are using bash, this entry file is usually your ~/.bashrc)"
echo ""
echo "info: please run 'neujahr.py add' to add some data"

if [[ ! :$PATH: == *:"$LOCATION":* ]]; then
	echo "warning: the directory we installed neujahr.py to is not on the PATH."
	echo "         for the program to work, this is required."
	echo "         please add the directory to the PATH variable."
	echo "         the directory: $LOCATION"
	echo "tip: in bash, you can add this line to your bashrc:"
	echo ""
	echo "  export PATH=\"$PATH:$LOCATION\""
	echo ""
fi
