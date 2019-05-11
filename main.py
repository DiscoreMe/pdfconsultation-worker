

from flask import Flask, redirect, flash, request, url_for
from werkzeug.utils import secure_filename
import os
import json
import pdfrw
from pdfrw import PdfDict

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload'

app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024
app.config["SECRET_KEY"] = "123456"

ALLOWED_EXTENSIONS = set(['pdf', 'txt', "json"])

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

        for file_document in js_conf["files"]:
            for file_request in request.files.values():
                if file_request.filename == file_document["filename"]:
                    template = pdfrw.PdfReader(file_document["filename"])
                    for field in file_document["fields"]:
                        for an in template.Root.Pages.Kids[0].Annots:
                            if an.T.to_unicode() == field["key"]:
                                an.update(PdfDict(V=field["value"]))
                    pdfrw.PdfWriter().write('output.pdf', template)
                        



    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run()