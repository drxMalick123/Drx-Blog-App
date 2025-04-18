from flask import Flask, render_template, request, redirect, url_for
import os


# Set allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if file extension is allowed
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_file(filename):
    # Get the file extension (after the last dot)
    ext = filename.split('.')[-1].lower()
    return ext in ALLOWED_EXTENSIONS

# Route for the upload page

# Route for handling the upload

def upload_file(app):
    if 'file' not in request.files:
        print('bimol')

        return redirect(request.url)
    
    file = request.files['file']
    # print(file.filename)
    if file and allowed_file(file.filename):
        # Secure the filename to prevent issues
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(f" app.con {app.config['UPLOAD_FOLDER'] }  name  {file.filename  } ")
        file.save(filename)
        
        # Store the file path in a variable and print it
        file_path = filename
        # print(f"File uploaded and stored at: {file_path}")
        print('bimol')
        # You can still return a response to the user
        return file_path
    else:
        return 'Invalid file format'


