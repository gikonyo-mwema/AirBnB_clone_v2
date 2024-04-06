#!/usr/bin/python3
"""
Fabric script to create a .tgz archive fromw contents of the web_static
folder and distribute it to web servers
"""

from fabric.api import local, env, put, run
from datetime import datetime
import os


# IPs of my web servers
env.hosts = ['54.157.151.166', '18.210.33.196']


def do_deploy(path):
	"""
	Distribute an archive to web servers.
	"""

	# Check if the file at the path archive_path exists
	if not os.path.exists(archive_path):
		return False

	try:
		# Upload the archive to the /tmp/ directory of the web server
		put(archive_path, '/tmp/')

		# Uncompress the archive to the folder
		# /data/web_static/releases on the web server
		filename = os.path.basename(archive_path)
		name, ext = os.path.splitext(filename)
		run('mkdir -p /data/web_static/releases/{}'.format(name))
		run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(filename, name))

		# Delete the archive from the web server
		run('rm /tmp/{}'.format(filename))

		# Delete the symbolic link /data/web_static/current from the web server
		# linke to th new version of your code
		run('ls -s /data/web_static/releases/{} /data/web_static/current'.format(name))

		return True
	except:
		return False
