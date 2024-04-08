#!/usr/bin/python3
"""
Fabric script that creates, distributes an archive to web servers,
and deletes out-of-date archives
"""

from datetime import datetime
from fabric.api import env, put, run, local, lcd, cd
import os

# replace with your servers' addresses
env.hosts = ["54.157.151.166", "18.210.33.196"]


def do_pack():
    """
    Generate a .tgz archive
    """
    local('mkdir -p versions')
    timestr = datetime.now().strftime('%Y%m%d%H%M%S')
    result = local('tar -cvzf versions/web_static_{0}.tgz \
web_static'.format(timestr))
    path = 'versions/web_static_{0}.tgz'.format(timestr)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print("web_static packed: {0} -> {1}Bytes".format(path, size))
    else:
        print("Failed to create the archive at {0}".format(path))
    if result.failed:
        return None
    else:
        return path


def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/')
        run('tar -xzf /tmp/{0} -C /data/web_static/releases/'.format(
            archive_path.split('/')[-1]))
        run('rm /tmp/{0}'.format(archive_path.split('/')[-1]))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{0} \
/data/web_static/current'.format(
            archive_path.split('/')[-1].replace('.tgz', '')))
        return True
    except Exception:
        return False


def deploy():
    """
    Create and distribute an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Delete out-of-date archives
    """
    number = int(number)
    if number < 2:
        number = 1
    else:
        number += 1

    with lcd('versions'):
        local('ls -t | tail -n +{0} | xargs rm -rf'.format(number))

    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{0} | xargs rm -rf'.format(number))
