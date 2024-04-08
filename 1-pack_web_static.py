#!/usr/bin/python3
"""
Fabric script create .tgz archive from contents of web_static
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generate a .tgz archive
    """

    # Create the version directory if it doesn't exist
    local('mkdir -p versions')

    # Generate the current time 
    timestr = datetime.now().strftime('%Y%m%d%H%M%S')

    # Create the archive
    result = local('tar -cvzf versions/web_static_{0}.tgz web_static'.format(timestr))

    path = 'versions/web_static_{0}.tgz'.format(timestr)

    # Check if the file exists before getting its size
    if os.path.exists(path):
        size = os.path.getsize(path)
        print("web_static packed: {0} -> {1}Bytes".format(path, size))
    else:
        print("Failed to create the archive at {0}".format(path))

    # Return the archive path if the archive has been generated
    if result.failed:
        return None
    else:
        return path

