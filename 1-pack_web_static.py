#!/usr/bin/python3
"""
Fabric script create .tgz archive from contents of web_static
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz archive
    """

    # Create the version directory if it doesn't exist
    local('mkdir -p versions')

    # Generate the .tgz archive
    timestr = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_{}.tgz'.format(timestr)

    result = local('tar -cvzf {} web_static'.format(path))

    # Return the archive path if the archive has beeen generated
    if result.failed:
        return None
    else:
        return path
