import json
import os
import random
import shutil
import string
import tarfile

import pdfrw
from flask import Flask, flash, redirect, request, send_file, url_for
from pdfrw import PdfDict
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload'

app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024
app.config["SECRET_KEY"] = "123456"

ALLOWED_EXTENSIONS = set(['pdf', "json"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        config = request.files.get("config")
        if config is None:
            return '', 500
        
        js_conf = json.loads(config.read())
        if js_conf['key'] != app.config["SECRET_KEY"]:
            return '', 403

        tmp_dir = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        os.mkdir(tmp_dir)
        files_output = []

        for file_document in js_conf["files"]:
            for file_request in request.files.values():
                if file_request.filename == file_document["filename"]:
                    if allowed_file(file_request.filename):
                        template = pdfrw.PdfReader(file_document["filename"])
                        for field in file_document["fields"]:
                            for an in template.Root.Pages.Kids[0].Annots:
                                if an.T.to_unicode() == field["key"]:
                                    an.update(PdfDict(V=field["value"]))
                        pdfrw.PdfWriter().write(os.path.join(tmp_dir, file_document["filename"]), template)
                        files_output.append(file_document["filename"])
        
        tar = tarfile.open('tmp.tar', 'w')
        for file in files_output:
            tar.add(os.path.join(tmp_dir, file))
        tar.close()

        shutil.rmtree(tmp_dir)

        return send_file('tmp.tar', mimetype="application/tar")

if __name__ == "__main__":
    app.run()
