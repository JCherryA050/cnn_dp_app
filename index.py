from flask import Flask, render_template, request, redirect, flash, url_for
import importlib
import sys
import urllib.request
# from appy import app
from werkzeug.utils import secure_filename
# from main import getPrediction
import os
import sys
sys.path.insert(0, '.')
from app import app
from main import getPrediction

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/', methods=['POST'])
# def submit_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No file selected for uploading')
#             return redirect(request.url)
#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#             getPrediction(filename)
#             acc = getPrediction(filename)
#             # flash(label)
#             flash(acc)
#             flash(filename)
#             return redirect('/')

# if __name__ == "__main__":
#     app.run()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('results.html', filename=getPrediction(filename))
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/new_image.png'), code=301)

@app.route('/display/<filename>')
def display_histogram(filename):
    	return redirect(url_for('static', filename='uploads/new_hist.png'), code=301)

if __name__ == "__main__":
    app.run()