#!/usr/bin/python3
"""Distribute an archive to web servers."""
import os
from time import strftime
from fabric.api import env, local, put, run, runs_once


env.hosts = ["54.166.118.64", "54.164.92.22"]


@runs_once
def do_pack():
    """Archive the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    file_timestamp = strftime("%Y%m%d%H%M%S")
    filename = f"versions/web_static_{file_timestamp}.tgz"
    try:
        local("tar -cvzf {} web_static".format(filename))
        filesize = os.stat(filename).st_size
    except Exception:
        filename = None
    return filename


def do_deploy(archive_path):
    """Deploy archive to remote server."""
    if not path.exists(archive_path):
        return False

    filename = path.basename(archive_path)
    dirname = filename.replace(".tgz", "")
    dirpath = f"/data/web_static/releases/{dirname}/"
    success = False

    try:
        put(archive_path, "/tmp/{}".format(filename))
        run(f"mkdir -p {dirpath}")
        run(f"tar -xzf /tmp/{filename} -C {dirpath}")
        run(f"rm -rf /tmp/{filename}")
        run(f"mv {dirpath}web_static/* {dirpath}")
        run(f"rm -rf {dirpath}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {dirpath} /data/web_static/current")
        print("Deployment successful")
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """Archive and deploy new version."""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


def do_clean(number=0):
    """Delete outdated archives."""
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
