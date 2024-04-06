#!/usr/bin/python3
"""
Fabric script to create a .tgz archive from the contents of the web_static
folder and distribute it to web servers.
"""

from fabric.api import local, env, put, run
from os.path import exists

# IPs of your web servers
env.hosts = ['54.157.151.166', '18.210.33.196']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    """

    # Check if the file at the path archive_path exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        
        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        # on the web server
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            filename, no_ext))

        # Move the uncompressed files from the web_static subdirectory
        # to the parent directory
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(no_ext, no_ext))

        # Delete the web_static subdirectory after moving the uncompressed files
        run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server,
        # linked to the new version of your code
        # (/data/web_static/releases/<archive filename without extension>)
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(no_ext))

        return True
    except Exception:
        return False
