from flask import *
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def processImage(filename, operation):
    print(f"The file name is {filename}\nThe operation is {operation}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f"static/{filename}", imgProcessed)
            return filename
        case "cwebp":
            cv2.imwrite(f"static/{filename.split('.')[0]}.webp", img)
            print(f"static/{filename.split('.')[0]}.webp")
            return f"{filename.split('.')[0]}.webp"
        case "cpng":
            cv2.imwrite(f"static/{filename.split('.')[0]}.png", img)
            return f"{filename.split('.')[0]}.png"
        case "cjpg":
            cv2.imwrite(f"static/{filename.split('.')[0]}.jpg", img)
            return f"{filename.split('.')[0]}.jpg"


@app.route("/")
def home():
    return render_template("index.html")


# A very simple Flask Hello World app for you to get started with...

@app.route("/about")
def about():
    return render_template("about.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = processImage(filename, operation)
            flash(
                f"The image has been processed and is available here <a href='/static/{filename}' target='_blank'> here </a>")
            return render_template("index.html")
    return render_template("index.html")


@app.route("/how")
def how():
    return render_template("how.html")

# adding comment


@app.route("/contact")
def contact():
    return render_template("contact.html")
