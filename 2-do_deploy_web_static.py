#!/usr/bin/python3
"""Deploy archives to remote servers."""
from os import path
from time import strftime
from fabric.api import env, local, put, run


env.hosts = ["54.166.118.64", "54.164.92.22"]


def do_deploy(archive_path):
    """Deploy archive to remote server."""
    if not os.path.exists(archive_path):
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
