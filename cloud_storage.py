import os

import dropbox

from dropbox import exceptions as ex
from dotenv import load_dotenv

import settings as setts

load_dotenv()


def dropbox_connect():
    """Create a connection to Dropbox"""
    access_token = os.environ.get('ACCESS_TOKEN')
    app_key = os.environ.get('KEY')
    app_secret = os.environ.get('APP_SECRET')
    try:
        dbx = dropbox.Dropbox(access_token, app_key=app_key, app_secret=app_secret)
        return dbx
    except ex.AuthError:
        return False


def download_file(dropbox_file_path: str):
    """
    Download single file from cloud storage

    :param dropbox_file_path: path to the file on cloud storage
    :type dropbox_file_path: str
    """
    dbx = dropbox_connect()
    if not dbx:
        return setts.connection_ex
    if auth_valid(dbx):
        try:
            metadata, result = dbx.files_download(path=dropbox_file_path)
            if result.reason == "OK":
                return {
                    "status": result.reason, "metadata": metadata,
                    "result": result,
                }
            return setts.request_ex
        except ex.ApiError as exc:
            return {
                "status": 400,
                "error": f"{exc.error.other} File '{dropbox_file_path}' does not exist"
            }
    return setts.auth_ex


def upload_file(file: bytes, file_to: str):
    """
    Upload a file to Dropbox storage

    :param file: file that you want to upload
    :type file: bytes

    :param file_to: path were you want to save file
    :type file_to:str

    """
    dbx = dropbox_connect()
    if not dbx:
        return setts.connection_ex
    if auth_valid(dbx):
        try:
            metadata = dbx.files_upload(file, file_to)
            return {
                "status": "OK", "file_name": metadata.name,
                "id": metadata.id, "path": metadata.path_display
            }
        except ex.ApiError as dbx_ex:
            return {"status": 400, "error": dbx_ex.error}
            # dropbox.files.UploadError
    return setts.auth_ex


def auth_valid(dbx):
    """Check that the access token is valid"""
    try:
        dbx.users_get_current_account()
        return True
    except ex.AuthError:
        return False
    except ex.BadInputError:
        return False


def build_path(path: str, name=None):
    """Build path
    :param name: file name
    :type name: str

    :param path: user path
    :type path: str
    """
    clean_path = ""
    path_list = path.replace("\\", "/").split("/")
    for path in path_list:
        if path != "":
            clean_path += f"/{path}"
    if clean_path:
        path = clean_path
        if name is not None:
            path = f"{clean_path}/{name}"
        return path


# def allowed_file(filename):
#     """Check file extension
#     :param filename: file name with extension
#     :type filename: str
#     """
#     allow = '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in setts.ALLOWED_EXTENSIONS
#     return allow
