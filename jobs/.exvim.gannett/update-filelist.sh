#!/bin/bash
export DEST="./.exvim.gannett"
export TOOLS="/Users/pli/exvim//vimfiles/tools/"
export IS_EXCLUDE=
export FOLDERS=""
export FILE_SUFFIXS=".*"
export TMP="${DEST}/_files"
export TARGET="${DEST}/files"
export ID_TARGET="${DEST}/idutils-files"
sh ${TOOLS}/shell/bash/update-filelist.sh
