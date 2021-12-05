import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import PyPDF2

UPLOAD_FOLDER = '/home/aadil_jamal/Desktop/cautious-octo-winner/static/uploads/'
ALLOWED_EXTENSIONS = { 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename=''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('output_result',
                                    filename=filename))
    return render_template("upload.html")
@app.route('/output_result', methods=['GET', 'POST'])
def output_result():
    if request.method == 'POST':
        if len(os.listdir(UPLOAD_FOLDER) ) == 0:
            return '<p>please upload_file firs</p>' 
        else:
            paths = os.listdir(UPLOAD_FOLDER)[0]
            
            pdf_in = open('/home/aadil_jamal/Desktop/cautious-octo-winner/static/uploads/Belnap.pdf', 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_in)
            pdf_writer = PyPDF2.PdfFileWriter()
            pagenumber = int(request.form.get("page"))#
            angle = int(request.form.get("rotate"))
            for pagenum in range(pdf_reader.numPages):
                if pagenum == pagenumber-1:
                    page = pdf_reader.getPage(pagenum)
                    page.rotateClockwise(angle)
                    pdf_writer.addPage(page)
                else:
                    page = pdf_reader.getPage(pagenum)
                    pdf_writer.addPage(page)
            pdf_out = open(f'{UPLOAD_FOLDER}rotated.pdf', 'wb')
            pdf_writer.write(pdf_out)
            pdf_out.close()
            pdf_in.close()
            rotated_file_path = os.path.dirname(f'{UPLOAD_FOLDER}rotated.pdf')+'/rotated.pdf'
            return rotated_file_path
    return  render_template("output_result.html")
                   


if __name__ == '__main__':
    app.run(debug=True)