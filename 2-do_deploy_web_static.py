#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import env, put, run
import os

env.hosts = ["54.157.151.166", "18.210.33.196"]


def do_deploy(archive_path):
    """
    Distribute archive.
    """

    # Check if the file at the path exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases directory
        run('mkdir -p /data/web_static/releases/')
        run('tar -xzf /tmp/{0} -C /data/web_static/releases/'.format(
            archive_path.split('/')[-1]))

        # Delete the archive from the web server
        run('rm /tmp/{0}'.format(archive_path.split('/')[-1]))

        # Delete the symbolic link /data/web_static/current from web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on  webserver,
        # linked to the new version (/data/web_static/releases/<archive name>
        run('ln -s /data/web_static/releases/{0} \
        /data/web_static/current'.format(
            archive_path.split('/')[-1].replace('.tgz', '')))
        return True
    except Exception:
        return False
