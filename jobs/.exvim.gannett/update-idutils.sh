#!/bin/bash
export DEST="./.exvim.gannett"
export TOOLS="/Users/pli/exvim//vimfiles/tools/"
export TMP="${DEST}/_ID"
export TARGET="${DEST}/ID"
sh ${TOOLS}/shell/bash/update-idutils.sh
