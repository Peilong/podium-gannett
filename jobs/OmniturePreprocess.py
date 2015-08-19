#!/usr/bin/python
# Import dependencies and libs
import psycopg2
import sys
import pprint
import os
import glob
import requests
import time
from datetime import datetime
import json

# Global Variables
PodiumApp = dict(
        hostname="172.21.6.66",
        port="4675",
        app="podium",
        appuser="podium",
        apppasswd="nvs2014!",
        database="podium_md_mapr_prod",
        dbuser="postgres",
        dbpasswd="password"
        )
EntitySourceId=125
entitySnames = ['BROWSER', 'BROWSER_TYPE','COLOR_DEPTH',
    'CONNECTION_TYPE','COUNTRY','DESKTOP','EVENT',
    'JAVASCRIPT_VERSION','LANGUAGES','MOBILE',
    'OPERATING_SYSTEMS','PLUGINS','REFERRER_TYPE',
    'RESOLUTION', 'SEARCH_ENGINES']
FileList = {'lookup_tar_file': "lookup_tar_file",
        'mobile_file_list': "mobile_file_list",
        'desktop_file_list': "desktop_file_list"}

######################################
# Name: Main() Function
# Input: None
# Output: None
# Function: Main entry to the program
######################################
def main():
    # Preprocess Start
    starttime = time.time()

    # Step 1: export environment Variables
    printStepHeader(1, "Find Env Variables")
    DirList = exportEnvVar()

    # Step 2: cleanup working directories
    printStepHeader(2, "Clean up Working Dir")
    #cleanupDir(DirList)
    
    # Step 3: copy and untar files into working dir:
    printStepHeader(3,"Copy and Untar Files")
    #cpyAndUntar(DirList,FileList)

    # Step 4: login PodiumApp & start REST reqest session
    printStepHeader(4, "Start REST Session")
    s = startRestSession()

    # Step 5: update entities in Postgres DB
    printStepHeader(5, "Update Entities in DB")
    updateEntities( s, getEntityIdList(getEntityObjectList(s,EntitySourceId)) )

    # Preprocess End
    endtime = time.time()

    # Calculate Total Runtime:
    print "\nTotal Proprocessing Time: %f seconds" % (endtime - starttime)

######################################
# Function: getEntityId(EntitySname)
# Input: String EntitySname
# Output: long EntityId
######################################
def getEntityId(EntitySname):
    conn_string = "host="+PodiumApp.get("hostname")+\
            " dbname="+PodiumApp.get("database")+\
            " user="+PodiumApp.get("dbuser")+\
            " password="+Podium.get("dbpasswd")
    # print "Connecting to database -->\n...%s" % (conn_string)
  
    # get a connection, if a connect cannot be made an exception 
    # will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this 
    # cursor to perform queries
    cursor = conn.cursor()

    # execute our query for entity ID
    cursor.execute("SELECT pe.nid FROM podium_core.pd_entity AS pe "+
            "JOIN podium_core.pd_source AS ps "+
            "ON ps.nid = pe.source_nid "+
            "WHERE UPPER(pe.sname) = UPPER('%s') " % (EntitySname)+
            "AND pe.entity_type = 'EXTERNAL'" )
    returnlist = cursor.fetchall()
    if returnlist:
        return returnlist[0][0]
    else:
        print "Entity sname "+EntitySname+\
                " not found!\nData preparation aborted!"
        exit(1)

########################################################
# Name: getEntityObjectList(restSession, EntitySourceId)
# Input: 1. A REST session Object
#        2. A single Entity Source ID
# Output: A list of Entity Objects (json formatted)
# Function: get a list of entity objects from
#           a single entity source ID
########################################################
def getEntityObjectList(restSession, EntitySourceId):
    url = "http://" + PodiumApp.get("hostname") + ":" +\
        PodiumApp.get("port") + "/" + PodiumApp.get("app") + "/"
    sourceType = "entity/external/entitiesBySrc/%d" % EntitySourceId
    entityObjectList = restSession.get(url + sourceType)
    if entityObjectList == "":
        print "EnityObjectList is empty!"
        print "Preprocess is aborted ..."
        exit(1)
    else:
        return  str(entityObjectList.text)

#########################################
# Name: getEntityIdList(entityObjectList)
# Input: A string of entity objects
# Output: A list of Entity IDs
# Function: get a list of entity IDs from
#           a list of entity snames
#########################################
def getEntityIdList(entityObjectList):
    entityIdList = []
    entityObjectDict = json.loads(entityObjectList)
    entityObjectDictSubList = entityObjectDict.get("subList")

    for idx, item in enumerate(entityObjectDictSubList):
        entityIdList.append(item.get("id"))
    
    if not entityIdList:
        print "Entity ID list is empty!"
        print "Preprocess is aborted ..."
        exit(1)
    else:
        return entityIdList

#########################################
# Name: startRestSession()
# Input: None
# Output: A REST request session object
# Function: Start a REST session and 
#           login
#########################################
def startRestSession():
    url = "http://" + PodiumApp.get("hostname") + ":" +\
        PodiumApp.get("port") + "/" + PodiumApp.get("app") + "/"
    securityUrl = url + "j_spring_security_check"

    # Start a request session
    s = requests.session()
    login_data = dict(
            j_username=PodiumApp.get("appuser"), 
            j_password=PodiumApp.get("apppasswd")
            )
    
    # Post a login request to Podium App
    loginResponse = s.post(securityUrl, data=login_data)
    loginResponseText = loginResponse.text

    # If login success, then return the REST request session object
    if not "login" in loginResponseText:
        print "Start REST Request Session Successfully!"
        return s
    # If not login, then report error and exit
    else:
        print "Invalid username or password....!!"
        exit(1)

#########################################
# Name: updateEntity(EntityId)
# Input: 1. A REST session object
#        2. A single Entity ID
# Output: None
# Function: Update the Podium Postgres
#           DB with a single EntityId
#########################################
def updateEntity(restSession, EntityId):
    url = "http://" + PodiumApp.get("hostname") + ":" +\
        PodiumApp.get("port") + "/" + PodiumApp.get("app") + "/"

    headers = {'content-type': 'application/json'}
    sourceType = "entity/loadDataForEntity/true"
    
    # Generate the payloadList
    payload = dict(
            loadTime=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), 
            entityId=str(EntityId)) 
    #print payload

    ret = restSession.put(url + sourceType,
            data=json.dumps(payloadList), headers=headers)
    if "Error" in (ret.text):
        print "Update Entities Failed!..."
        print "Preprocess is aborted ..."
        exit(1)
    else:
        return


#########################################
# Name: updateEntities(EntityList)
# Input: 1. A REST session object
#        2. A list of Entity IDs
# Output: None
# Function: Update the Podium Postgres
#           DB with a list of EntityIds
#########################################
def updateEntities(restSession, EntityList):
    url = "http://" + PodiumApp.get("hostname") + ":" +\
        PodiumApp.get("port") + "/" + PodiumApp.get("app") + "/"

    headers = {'content-type': 'application/json'}
    sourceType = "entity/loadDataForEntities/true"
    
    # Generate the payloadList
    payloadList = []
    for idx, entityId in enumerate(EntityList):
        payloadList.append( dict(
            loadTime=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), 
            entityId=str(entityId)) )
    #print "Payload List:\n"+str(payloadList)

    ret = restSession.put(url + sourceType,
            data=json.dumps(payloadList), headers=headers)
    if "Error" in (ret.text):
        print "Update Entities Failed!..."
        exit(1)
    else:
        return
     
##########################################
# Name: exportEnvVar():
# Input: none
# Output: dict(DIR_NAME: DIR_VALUE, ...)
# Function: export the env vars
##########################################
def exportEnvVar():
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
    
    return dict(SCRIPT_WORKING_DIR=SCRIPT_WORKING_DIR,
            PROJECT_DIR=PROJECT_DIR,
            FTP_LANDING_DIR=FTP_LANDING_DIR,
            LOOKUP_WORKING_DIR=LOOKUP_WORKING_DIR,
            MOBILE_WORKING_DIR=MOBILE_WORKING_DIR,
            DESKTOP_WORKING_DIR=DESKTOP_WORKING_DIR)

#######################################
# Name: cleanupDir()
# Input: dict(directory list)
# Output: None
# Function: Cleanup working directories
#######################################
def cleanupDir(DirList):
    # If a directory is not empty, then clean the directory
    if os.listdir( DirList.get('LOOKUP_WORKING_DIR') ):
        print 'Cleaning up lookup working directory ...'
        os.system('rm -r '+DirList.get('LOOKUP_WORKING_DIR')+'/*')
    if os.listdir( DirList.get('MOBILE_WORKING_DIR') ):
        print 'Cleaning up mobile working directory ...'
        os.system('rm -r '+DirList.get('MOBILE_WORKING_DIR')+'/*')
    if os.listdir( DirList.get('DESKTOP_WORKING_DIR') ):
        print 'Cleaning up desktop working directory ...'
        os.system('rm -r '+DirList.get('DESKTOP_WORKING_DIR')+'/*')

#####################################
# Name: cpyAndUntar()
# Input: 1. dict(directory list)
#        2. dict(filelist)
# Output: None
# Function: Copy lately loaded data
# into working directories and untar
# them if tarred
#####################################
def cpyAndUntar(DirList, FileList):
    # Define a filelist List as local variable
    filelist = []
    # Open lookup_tar_file and read all wildcard files
    with open(FileList.get('lookup_tar_file')) as f:
        content = f.read().splitlines()
    # Append all wildward file names into the filelist
    for line in content:
        filelist.append(DirList.get('FTP_LANDING_DIR')+'/'+line)
    # Replace wildcard file names into full names and then copy, untar
    for wildcardfile in filelist:
        for full_name in glob.glob(wildcardfile):
            os.system('cp '+full_name+' '+DirList.get('LOOKUP_WORKING_DIR'))
            os.system('tar -xvf '+full_name+' -C '+DirList.get('LOOKUP_WORKING_DIR'))

    # Clear filelist
    filelist = []
    # Open desktop_file_list and read all wildcard files
    with open(FileList.get('desktop_file_list')) as f:
        content = f.read().splitlines()
    # Append all wildcard file names into the filelist
    for line in content:
        filelist.append(DirList.get('FTP_LANDING_DIR')+'/'+line)
    # Replace wildcard file names into full names and then Copy
    for wildcardfile in filelist:
        for full_name in glob.glob(wildcardfile):
            os.system('cp '+full_name+' '+DirList.get('DESKTOP_WORKING_DIR'))

    # Clear filelist
    filelist = []
    # Open desktop_file_list and read all wildcard files
    with open(FileList.get('mobile_file_list')) as f:
        content = f.read().splitlines()
    # Append all wildcard file names into the filelist
    for line in content:
        filelist.append(DirList.get('FTP_LANDING_DIR')+'/'+line)
    # Replace wildcard file names into full names and then copy, untar
    for wildcardfile in filelist:
        for full_name in glob.glob(wildcardfile):
            os.system('cp '+full_name+' '+DirList.get('MOBILE_WORKING_DIR'))

#######################################
# Name: printStepHeader(number, title)
# Input: 1. The step number integer
#        2. The step title String
# Output: The string of step header
# Function: Print the step header info
#           to console
#######################################
def printStepHeader(number, title):
    titlecat = "* Step "+\
            str(number)+\
            ": "+\
            title+\
            " *"
    print "\n" + \
            len(titlecat)*'*'+\
            "\n"+\
            titlecat+\
            "\n"+\
            len(titlecat)*'*'

if __name__ == "__main__":
    main()
