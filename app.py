import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, send_file, render_template
from bg_removal import process

UPLOAD_FOLDER = 'uploads/'
#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upload API
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("uploaded_path: ", uploaded_path)
            print("saved file successfully")
            bg_removed_filename = process(uploaded_path, app.config['UPLOAD_FOLDER'])
            os.remove(uploaded_path)
            bg_removed_filename = bg_removed_filename.split('/')[1]
            print("bg_removed_filename: ", bg_removed_filename)
            #send file name as parameter to download
            return redirect('/downloadfile/'+ bg_removed_filename)
    return render_template('upload_file.html')

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
    app.run(debug=False, threaded=True)