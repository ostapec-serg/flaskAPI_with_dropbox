import io

from flask import Flask, Response
from flask import request, send_file
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

import cloud_storage
import settings as setts

app = Flask(__name__)
api = Api()


class CloudData(Resource):
    """ """
    def get(self):
        file_path = request.args.get("path", "")
        if request.method == "GET":
            if not isinstance(file_path, str):
                return setts.type_ex
            if file_path == "":
                return setts.path_ex
            path = cloud_storage.build_path(path=file_path)
            if path:
                file_path = path
            response = cloud_storage.download_file(file_path)
            if response["status"] == "OK":
                file = response["result"].content
                name = response["metadata"].path_display
                return send_file(io.BytesIO(file), as_attachment=True, download_name=name)
            return Response(
                response["error"], status=response["status"],
                mimetype='application/json'
                )

    def put(self):
        if request.method == "PUT":
            if 'file' not in request.files:
                return Response(
                    "No file part", status=400,
                    mimetype='application/json'
                )
            if request.files["file"].filename == '':
                return Response(
                    "No file name", status=400,
                    mimetype='application/json'
                )
            if request.files["file"]:
                file = request.files["file"].read()
                name = secure_filename(request.files["file"].filename)
                if isinstance(file, bytes) and isinstance(name, str):
                    path = f"/{name}"
                    if 'path' in request.form:
                        path = cloud_storage.build_path(name, request.form['path'])
                    response = cloud_storage.upload_file(file, path)
                    if response["status"] == "OK":
                        return response
                return Response(
                    "Invalid type", status=400,
                    mimetype='application/json'
                )


api.add_resource(CloudData, "/api/files/")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
