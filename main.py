import flask
import hashlib
import os
import re

from flask import Flask, jsonify, request, send_file

upload_app = Flask(__name__)
upload_app.config["DEBUG"] = True

BUF_SIZE = 65536
STORAGE_DIRECTORY = os.path.join(upload_app.root_path, "store")

@upload_app.route('/', methods=['GET'])
def get():
    if "hash" not in request.args:
        raise RuntimeError("hash required")

    hash = request.args.get("hash")

    if re.match(r'^[0-9a-f]*$', hash) is None:
        raise RuntimeError("provided hash is not valid, must be hex")

    folder_name = hash[0:2]
    file_path = os.path.join(STORAGE_DIRECTORY, folder_name, hash)

    if not os.path.exists(file_path):
        raise RuntimeError("file does not exists")

    return send_file(os.path.abspath(file_path), hash)


@upload_app.route('/', methods=['POST'])
def post():
    if len(request.files) == 0 or "file" not in request.files:
        raise RuntimeError("no files provided")

    file = request.files.get("file")

    sha1 = hashlib.sha1()
    tmp_file_path = os.path.join(STORAGE_DIRECTORY, "tmp")

    with open(tmp_file_path, "wb") as tmp:
        while True:
            data = file.read(BUF_SIZE)

            if not data:
                break

            sha1.update(data)
            tmp.write(data)

    hash = sha1.hexdigest()

    dir_path = os.path.join(STORAGE_DIRECTORY, hash[0:2])

    if not (os.path.exists(dir_path)):
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path, hash)

    if not os.path.exists(file_path):
        os.rename(tmp_file_path, file_path)
    else:
        os.remove(tmp_file_path)

    print(file_path)

    return jsonify(hash)


@upload_app.route('/', methods=['DELETE'])
def delete():
    if "hash" not in request.args:
        raise RuntimeError("hash required")

    hash = request.args.get("hash")

    if re.match(r'^[0-9a-f]*$', hash) is None:
        raise RuntimeError("provided hash is not valid, must be hex")

    dir_path = os.path.join(STORAGE_DIRECTORY, hash[0:2])
    file_path = os.path.join(dir_path, hash)

    if not os.path.exists(file_path):
        raise RuntimeError("file does not exists")

    os.remove(file_path)

    if len(os.listdir(dir_path)) == 0:
        os.rmdir(dir_path)

    return jsonify(True)



if __name__ == '__main__':
    upload_app.run()
