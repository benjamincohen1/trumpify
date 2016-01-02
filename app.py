from flask import Flask, render_template
app = Flask(__name__)
import httplib

from flask import Flask, abort, render_template, request
from flask.ext.uploads import (UploadSet, configure_uploads, IMAGES,
        UploadNotAllowed)
from werkzeug import secure_filename

UPLOADED_PHOTOS_DEST = '/tmp/photos'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16MB
app.config.from_object(__name__)

uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

def allowed_file(filename):
    True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        try:
            filename = uploaded_photos.save(request.files.get('file'))
        except UploadNotAllowed:
            abort(httplib.BAD_REQUEST)

        return ''

    abort(httplib.BAD_REQUEST)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
