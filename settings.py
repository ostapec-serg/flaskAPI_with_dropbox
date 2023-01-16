from flask import Response


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Exception msgs
connection_ex = {"status": 400, "error": "ConnectionError"}
request_ex = {"status": 400, "error": "Bad request"}
auth_ex = {"status": 401, "error": "auth failed"}
type_ex = Response("Invalid type", status=400, mimetype='application/json')
path_ex = Response("Parameter 'path' is empty", status=400, mimetype='application/json')
