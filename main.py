import pdfrw
from pdfrw import PdfDict

template = pdfrw.PdfReader('test_form.pdf')

ans = template.Root.Pages.Kids[0].Annots[0].update(PdfDict(V='(test)'))


pdfrw.PdfWriter().write('output.pdf', template)

fs = template.Root.AcroForm.Fields

for f in fs:
    print(f.Kids)
    print(f.T.decode())
    

from flask import Flask, redirect, flash, request, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload'
ALLOWED_EXTENSIONS = set(['pdf', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.form)
        return ''
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # secure_filename will return a secure version of it. 
            # This filename can then safely be stored on a regular file system and passed to os.path.join().
            # The filename returned is an ASCII only string for maximum portability.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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