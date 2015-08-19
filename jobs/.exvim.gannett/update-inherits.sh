#!/bin/bash
export DEST="./.exvim.gannett"
export TOOLS="/Users/pli/exvim//vimfiles/tools/"
export TMP="${DEST}/_inherits"
export TARGET="${DEST}/inherits"
sh ${TOOLS}/shell/bash/update-inherits.sh
