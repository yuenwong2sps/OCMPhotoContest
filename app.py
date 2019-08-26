import os
from flask import Flask, flash, render_template, request, url_for, send_from_directory
from werkzeug import secure_filename

from shutil import copyfile

import glob

from flask import jsonify

import DetectFace

import gallery

import PhotoContestDB

import sqlite3

import datetime

UPLOAD_FOLDER = 'ContestPhoto/'
UPLOAD_FOLDER_Preview = 'ContestPhotoPreview/'
UPLOAD_FOLDER_TMP = 'ContestPhotoTemp/'
DBPATH = "./db/pythonsqlite.db"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_TMP'] = UPLOAD_FOLDER_TMP
app.config['UPLOAD_FOLDER_Preview'] = UPLOAD_FOLDER_Preview

#gallery = view smaller images for preview
glly = gallery.Gallery(app.config['UPLOAD_FOLDER_Preview'])






@app.route("/")
def index_page():
    return render_template('index.html')


@app.route('/upload')
def upload_file_page():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def uploaderRequest():

    print(request.form)

    if request.method == 'POST':
        #funcWord = request.form['task']


        if 'txtPhoneNumber' not in request.form:

            flash('No user phone number')
            return redirect(request.url)

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

        #if file and allowed_file(file.filename):
        #get file extension
        tmpName = str(file.filename)
        ext_tmpName = tmpName[-1*(len(tmpName) - (tmpName.rfind("."))):]

        currentDT = datetime.datetime.now()

        timestamp_str = (str(currentDT.strftime("%Y%m%d%H%M%S"))+str(currentDT.microsecond))

        #tmp file name format: tmp_datetime_telNumber.JPG
        tmpImageName = "tmp_" + timestamp_str + "_" + request.form['txtPhoneNumber'] + ext_tmpName

        phoneNumberList = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*_" + request.form['txtPhoneNumber'] + "_*"))

        if file and allowed_file(tmpImageName):
            filename = secure_filename(tmpImageName)


            #save original image as temp
            file.save(os.path.join(app.config['UPLOAD_FOLDER_TMP'], "ori_" + filename))

            #detect number of face with original image
            num_of_face = DetectFace.DetectNumOfFace(os.path.join(app.config['UPLOAD_FOLDER_TMP'], "ori_" + filename))

            #resize the orginal image for larger screen, fixed size
            DetectFace.ResizeAndSave(os.path.join(app.config['UPLOAD_FOLDER_TMP'], "ori_" + filename), os.path.join(app.config['UPLOAD_FOLDER_TMP'], filename))

            #print(os.path.join(app.config['UPLOAD_FOLDER_TMP'], filename))

            os.remove(os.path.join(app.config['UPLOAD_FOLDER_TMP'], "ori_" + filename))

            return jsonify(ofilename = filename, onum_of_face = num_of_face, opreviousFileNo= len(phoneNumberList), ouploadtime = timestamp_str )

        else:
            flash('Fail to save')
            return redirect(request.url)


    else:
        lash('Bad Request')
        return redirect(request.url)

@app.route('/uploaderSave', methods = ['GET', 'POST'])
def uploaderSaveRequest():

    print(request.form)

    if request.method == 'POST':
        #funcWord = request.form['task']

        #take filename, and fellowship mapping info and save

        if 'txtTMPfile' not in request.form:

            flash('No tmp file')
            return redirect(request.url)

        if 'txtpreviousFileNo' not in request.form:

            flash('No file number')
            return redirect(request.url)


        #previous file number
        ipreviousFileNo = int(request.form['txtpreviousFileNo'])


        #Remove tmp_ from filename
        tmpImageName = request.form['txtTMPfile']

        tmpImageName = tmpImageName[4:len(tmpImageName)]

        tmpImageName_wo_ext = tmpImageName[:(tmpImageName.rfind("."))]

        ext_tmpName = "_" + str(ipreviousFileNo + 1) + tmpImageName[-1*(len(tmpImageName) - (tmpImageName.rfind("."))):]

        tmpImageName = tmpImageName_wo_ext + ext_tmpName


        #image copy and resize from tmp folder to regular folder

        if allowed_file(tmpImageName):
            filename = secure_filename(tmpImageName)


            copyfile(os.path.join(app.config['UPLOAD_FOLDER_TMP'], request.form['txtTMPfile']), os.path.join(app.config['UPLOAD_FOLDER'], filename))


            #resize the orginal image for smaller preview, fixed size
            DetectFace.ResizeAndSavePreview(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER_Preview'], filename))

            os.remove(os.path.join(app.config['UPLOAD_FOLDER_TMP'], request.form['txtTMPfile']))


            try:

                tel = request.form['txtPhoneNumber']
                uploadtime = request.form['txtUploadTime']
                photoPath = filename

                with sqlite3.connect(DBPATH) as con:
                    for i in range(5):

                        fellowship = request.form['txtFellowship' + str(i+1)]
                        tagName = request.form['txtTagName' + str(i+1)]
                        print(request.form['txtFellowship' + str(i+1)] + ":" + request.form['txtTagName' + str(i+1)])
                        if len(fellowship) > 0 and len(tagName) > 0:
                            cur = con.cursor()
                            cur.execute("INSERT into PhotoEntries (uploadtime, tel, photoPath, fellowship, tagName) values (?,?,?,?,?)",(uploadtime,tel,photoPath,fellowship, tagName))

                            con.commit()

                            print("committed")

                    msg = "PhotoEntries successfully Added"

            except:
                con.rollback()
                msg = "We can not add the PhotoEntries to the list"

            print(msg)

            return jsonify(status = "Saved", messsage = msg)
            con.close()



        else:
            flash('Fail to save')
            return redirect(request.url)


    else:
        lash('Bad Request')
        return redirect(request.url)


@app.route('/img/<path:filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/imgtmp/<path:filename>')
def send_filetmp(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_TMP'], filename)

@app.route('/imgpre/<path:filename>')
def send_filepre(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_Preview'], filename)



@app.route('/gallery', methods = ['GET', 'POST'])
def dir_listing():

    gallerylist = glly.GetDequeFileList(20)

    return jsonify(ogallerylist = gallerylist)


@app.route("/view",  methods = ['GET', 'POST'])
def view():
    con = sqlite3.connect(DBPATH)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * from PhotoEntries")
    rows = cur.fetchall()

    return jsonify(results = rows)



#support functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == '__main__':
    app.run(debug = True)
    #app.run(host="0.0.0.0", port=80)
