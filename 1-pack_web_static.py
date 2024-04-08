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
    result = local(f'tar -cvzf versions/web_static_{timestr}.tgz web_static')

    path = f'versions/web_static_{timestr}.tgz'

    # Check if the file exists before getting its size
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"web_static packed: {path} -> {size}Bytes")
    else:
        print(f"Failed to create the archive at {path}")

    # Return the archive path if the archive has been generated
    if result.failed:
        return None
    else:
        return path

