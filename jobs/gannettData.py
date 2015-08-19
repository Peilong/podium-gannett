import os
import glob

##########################################
#  Step 1: Export Environment Variables  #
##########################################
print 30*'*'
print 'Step 1: Finding Env Variables'
print 30*'*'

# Script working Directory
SCRIPT_WORKING_DIR = os.getcwd();
print 'Script Working Directory: '+SCRIPT_WORKING_DIR

# Project Directory
PROJECT_DIR = os.path.dirname(SCRIPT_WORKING_DIR)
print 'Project Directory: ' + PROJECT_DIR

# FTP Landing Directory
FTP_LANDING_DIR = PROJECT_DIR +'/OmniTest'
if not os.path.exists(FTP_LANDING_DIR):
    print 'Creating FTP Landing Directory ...'
    os.makedirs(FTP_LANDING_DIR)
print 'FTP Landing Directory: ' + FTP_LANDING_DIR

# Lookup Working Directory
LOOKUP_WORKING_DIR = PROJECT_DIR+'/OmniTest/lookup_work'
if not os.path.exists(LOOKUP_WORKING_DIR):
    print 'Creating Lookup Working Directory ...'
    os.makedirs(LOOKUP_WORKING_DIR)
print 'Lookup Working Directory: ' + LOOKUP_WORKING_DIR

# Mobile Working Directory
MOBILE_WORKING_DIR = PROJECT_DIR + '/OmniTest/mobile_work'
if not os.path.exists(MOBILE_WORKING_DIR):
    print 'Creating Mobile Working Directory ...'
    os.makedirs(MOBILE_WORKING_DIR)
print 'Mobile Working Directory: ' + MOBILE_WORKING_DIR

# Desktop Working Directory
DESKTOP_WORKING_DIR = PROJECT_DIR + '/OmniTest/desktop_work'
if not os.path.exists(DESKTOP_WORKING_DIR):
    print 'Creating Desktop Working Directory ...'
    os.makedirs(DESKTOP_WORKING_DIR)
print 'Desktop Working Directory: ' + DESKTOP_WORKING_DIR

######################################
# Step 2: Clean up working directory #
######################################
print '\n'+30*'*'
print 'Step 2: Clean up working dir'
print 30*'*'
if os.listdir(LOOKUP_WORKING_DIR):
    print 'Cleaning up lookup working directory ...'
    os.system('rm -r '+LOOKUP_WORKING_DIR+'/*')
if os.listdir(MOBILE_WORKING_DIR):
    print 'Cleaning up mobile working directory ...'
    os.system('rm -r '+MOBILE_WORKING_DIR+'/*')
if os.listdir(DESKTOP_WORKING_DIR):
    print 'Cleaning up desktop working directory ...'
    os.system('rm -r '+DESKTOP_WORKING_DIR+'/*')

######################################
##  Step 3: Copy and Untar files  ####
######################################
print '\n'+30*'*'
print 'Step 3: Copy and Untar files'
print 30*'*'

with open('lookup_tar_file') as f:
    content = f.read().splitlines()

filelist = []
for line in content:
    filelist.append(FTP_LANDING_DIR+'/'+line)

for wildcardfile in filelist:
    for full_name in glob.glob(wildcardfile):
        #full_file_name.append(full_name)
        os.system('cp '+full_name+' '+LOOKUP_WORKING_DIR)
        os.system('tar -xvf '+full_name+' -C '+LOOKUP_WORKING_DIR)

with open('desktop_file_list') as f:
    content = f.read().splitlines()
for line in content:
    filelist.append(FTP_LANDING_DIR+'/'+line)
for wildcardfile in filelist:
    for full_name in glob.glob(wildcardfile):
        os.system('cp '+full_name+' '+DESKTOP_WORKING_DIR)

with open('mobile_file_list') as f:
    content = f.read().splitlines()
for line in content:
    filelist.append(FTP_LANDING_DIR+'/'+line)
for wildcardfile in filelist:
    for full_name in glob.glob(wildcardfile):
        os.system('cp '+full_name+' '+MOBILE_WORKING_DIR)

os.system('python load_desktop.py') 

'''
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

'''
