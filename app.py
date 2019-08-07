import os
from flask import Flask, flash, render_template, request, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = 'ContestPhoto/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index_page():
    return render_template('index.html')


@app.route('/upload')
def upload_file_page():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def routeRequest():
    if request.method == 'POST':
        #funcWord = request.form['task']
        funcWord = 'uploadPic'
        if funcWord:
            if funcWord == 'uploadPic':
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return 'file uploaded successfully'


@app.route('/img/<path:filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/gallery', methods = ['GET', 'POST'])
def dir_listing():

    # Joining the base and the requested path
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], '')

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    imagesPath = []

    for file in files:
        imagesPath.append("/img/" + file)

    return render_template('files.html', files=imagesPath)





#support functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.run(debug = True)
