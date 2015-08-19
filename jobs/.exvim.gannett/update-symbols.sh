#!/bin/bash
export DEST="./.exvim.gannett"
export TOOLS="/Users/pli/exvim//vimfiles/tools/"
export TMP="${DEST}/_symbols"
export TARGET="${DEST}/symbols"
sh ${TOOLS}/shell/bash/update-symbols.sh
