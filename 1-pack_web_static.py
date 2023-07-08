#!/usr/bin/python3
"""Compress web_static/."""
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """Generate a .tgz archive from `web_static/` directory."""
    file_timestamp = strftime("%Y%m%d%H%M%S")
    filename = f"versions/web_static_{file_timestamp}.tgz"
    try:
        local("mkdir -p versions")
        local(f"tar -czvf {filename} web_static/")
        return filename
    except Exception as ex:
        return None
