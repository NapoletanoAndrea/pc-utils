import os
import shutil
from urllib.request import urlretrieve
from urllib.parse import urlparse
import ftplib


def is_ftp(path: str) -> bool:
    return path.startswith("ftp://")


def parse_ftp_url(url):
    parsed = urlparse(url)
    return {
        "host": parsed.hostname,
        "port": parsed.port or 21,
        "user": parsed.username or "anonymous",
        "password": parsed.password or "",
        "path": parsed.path
    }


def ftp_connect(info):
    ftp = ftplib.FTP()
    ftp.connect(info["host"], info["port"])
    ftp.login(info["user"], info["password"])
    return ftp


def download_ftp_folder(ftp, remote_dir, local_dir):
    os.makedirs(local_dir, exist_ok=True)

    original_dir = ftp.pwd()
    ftp.cwd(remote_dir)

    for item_full_path in ftp.nlst():
        if item_full_path in (".", ".."):
            continue

        # Create local path
        local_path = os.path.join(local_dir, os.path.basename(item_full_path))

        try:

            # Try entering directory
            ftp.cwd(item_full_path)

            # It's a directory → recurse
            download_ftp_folder(ftp, ftp.pwd(), local_path)

            # Go back
            ftp.cwd("..")

        except ftplib.error_perm:
            # It's a file → download
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with open(local_path, "wb") as f:
                ftp.retrbinary(f"RETR {item_full_path}", f.write)

    ftp.cwd(original_dir)


def upload_ftp_folder(ftp: ftplib.FTP, local_dir, remote_dir):
    try:
        ftp.mkd(remote_dir)
    except:
        pass

    ftp.cwd(remote_dir)

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)

        if os.path.isdir(local_path):
            upload_ftp_folder(ftp, local_path, item)
            ftp.cwd("..")
        else:
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {item}", f)


def move_contents(src, dst):
    src_is_ftp = is_ftp(src)
    dst_is_ftp = is_ftp(dst)

    # ❌ FTP → FTP (skip for now)
    if src_is_ftp and dst_is_ftp:
        print("FTP to FTP transfer not supported")
        return

    # 📥 FTP → LOCAL
    if src_is_ftp:
        info = parse_ftp_url(src)
        ftp = ftp_connect(info)

        print(f"Downloading from FTP: {src}")
        download_ftp_folder(ftp, info["path"], dst)

        ftp.quit()
        print("Download complete!")
        return

    # 📤 LOCAL → FTP
    if dst_is_ftp:
        info = parse_ftp_url(dst)
        ftp: ftplib.FTP = ftp_connect(info)

        print(f"Uploading to FTP: {dst}")
        upload_ftp_folder(ftp, src, info["path"])

        ftp.quit()
        print("Upload complete!")
        return

    # 📁 LOCAL → LOCAL (your original logic)
    if not os.path.exists(src):
        print(f"Source path does not exist: {src}")
        return

    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        try:
            shutil.move(src_path, dst_path)
            print(f"Moved: {src_path} -> {dst_path}")
        except Exception as e:
            print(f"Failed to move {src_path}: {e}")
