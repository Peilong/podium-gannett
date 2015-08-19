export SCRIPT_WORKING_DIR=$PWD
. ./setup_env.sh

rm $LOOKUP_WORKING_DIR/*
rm $DESKTOP_WORKING_DIR/*
rm $MOBILE_WORKING_DIR/*

for fname in `cat lookup_tar_file`
   do
      cp $FTP_LANDING_DIR/$fname $LOOKUP_WORKING_DIR
      cd $LOOKUP_WORKING_DIR;tar -xvf $LOOKUP_WORKING_DIR/* 
   done
cd $SCRIPT_WORKING_DIR

for fname1 in `cat desktop_file_list`
   do
     cp $FTP_LANDING_DIR/$fname1 $DESKTOP_WORKING_DIR
   done



for fname2 in `cat mobile_file_list`
   do
     cp $FTP_LANDING_DIR/$fname2 $MOBILE_WORKING_DIR
   done

python < load_desktop.py
#python < load_mobile.py
#python < load_lookups.py

