"""Fabric file."""
from fabric import Connection
from os import path
from time import strftime
from sys import argv


def main():
    """Say hello world."""
    for host in ("ubuntu@54.166.118.64", "ubuntu@54.164.92.22"):
        c = Connection(
            host,
            connect_kwargs={"key_filename": "/home/kael/.ssh/school"})
        do_deploy(c)


def do_deploy(connection):
    """Deploy archive to remote server."""
    if len(argv) < 2:
        print("provide path to archive")
        return False

    archive_path = argv[1]
    if not path.exists(archive_path):
        print("can't find", archive_path)
        return False

    filename = path.basename(archive_path)
    dirname = filename.replace(".tgz", "")
    dirpath = f"/data/web_static/releases/{dirname}/"
    success = False

    try:
        connection.put(archive_path, f"/tmp/{filename}")
        connection.run(f"sudo mkdir -p {dirpath}")
        connection.run(f"sudo tar -xzf /tmp/{filename} -C {dirpath}")
        connection.run(f"sudo rm -rf /tmp/{filename}")
        connection.run(f"sudo mv {dirpath}web_static/* {dirpath}")
        connection.run(f"sudo rm -rf {dirpath}web_static")
        connection.run("sudo rm -rf /data/web_static/current")
        connection.run(f"sudo ln -s {dirpath} /data/web_static/current")
        print("Deployment successful")
        success = True
    except Exception:
        success = False
    return success


if __name__ == "__main__":
    main()
