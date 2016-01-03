import base64
import httplib
import os

from flask import (Flask, abort, render_template, redirect, request,
                   send_from_directory, url_for)
from flask.ext.uploads import (UploadSet, configure_uploads, IMAGES,
                               UploadNotAllowed)

from trump import trumpify

app = Flask(__name__)

UPLOADED_PHOTOS_DEST = '/tmp/photos'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16MB
app.config.from_object(__name__)

uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files)
    if 'file' in request.files:
        try:
            filename = uploaded_photos.save(request.files.get('file'))
            filename = os.path.join(UPLOADED_PHOTOS_DEST, filename)
            output_file = trumpify(filename)
        except UploadNotAllowed:
            abort(httplib.BAD_REQUEST)

        return url_for('view_raw', hash=output_file.replace('.png', ''))

    abort(httplib.BAD_REQUEST)


@app.route('/view/<hash>')
def view_output(hash):
    return render_template('view.html', hash=hash)


@app.route('/view/<hash>/raw')
def view_raw(hash):
    return send_from_directory(os.path.join(os.getcwd(), 'outs'),
                               '{}.png'.format(hash))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
