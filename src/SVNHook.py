#!/usr/bin/env python

import ConfigParser

config = ConfigParser.ConfigParser()
DELIMITER = ','
retVal = 0

def loadConfigFile( configFilePath ):
    config.read( configFilePath )

def command_output( cmd ):
    " Capture a command's standard output. "
    import subprocess
    return subprocess.Popen( 
      cmd.split(), stdout = subprocess.PIPE ).communicate()[0]

def checkRepositoryACL( configObj, repositoryName, userName ):
    """
        This method checks the cfg file for repository 
        listing and the groups mapped to the repository
    """
    groupName = configObj.get( "repositories", repositoryName )
    if ( groupName.find( DELIMITER ) == -1 ):
        retVal = checkUserACL( configObj, groupName, userName )
    else:
        for gName in groupName.split( DELIMITER ):
            retVal = checkUserACL( configObj, gName, userName )
            if ( retVal == 0 ):
                break
    return retVal


def checkUserACL( configObj, groupName, userName ):
    """
        This method checks for the username in the
        given groups
    """
    userNameList = configObj.get( "groups", groupName )
    if ( userNameList.find( userName.strip() ) == -1 ):
        sys.stderr.write( " {0} doesn't have access to given repository".format( userName ) )
        return 1
    else:
        return 0

def checkUserAccessToRepository( configFileName, repositoryName, userName ):
    """
        Method to verify the access for given user and repository
    """
    loadConfigFile( configFileName )
    return checkRepositoryACL( config, repositoryName, userName )


def authorizeUserAction( repositoryPath, txnVersion, configFileName ):
    svnlookString = '/usr/bin/svnlook author -t {0} {1}'.format( txnVersion, repositoryPath )
    authorName = command_output( svnlookString )
    return checkUserAccessToRepository( configFileName, repositoryPath, authorName )


if __name__ == "__main__":
    import sys
    repository = sys.argv[1]
    txn = sys.argv[2]
    configFile = sys.argv[3]
    sys.stdout.write( " repos :: {0} , txn :: {1} , config :: {2}".format( repository, txn, configFile ) )
    sys.exit( authorizeUserAction( repository, txn, configFile ) )




