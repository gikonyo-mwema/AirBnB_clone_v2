#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from web_static
and distributes it to web servers
"""

from fabric.api import run, put, env, local
from os.path import exists, isdir
import os

env.hosts = ['54.157.151.166', '18.210.33.196']


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

    # Print the stderr of the tar command
    print(result.stderr)

    # Return the archive path if the archive has been correctly generated
    if result.failed:
        return None
    else:
        return path


def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """

    # Check if the file at the path archive_path doesn’t exist
    if not exists(archive_path) or not isdir(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
        archive_filename = os.path.basename(archive_path)
        without_extension = os.path.splitext(archive_filename)[0]
        run("mkdir -p /data/web_static/releases/{}/".format(
            without_extension))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_filename, without_extension))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(
            without_extension))

        return True
    except:
        return False
