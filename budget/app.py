import os
from flask import Flask, render_template, request, redirect
from request import *
from wtforms import SubmitField
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("first.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/result')
def info():
    return render_template("result.html")


UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def read_x():
    a = pd.read_excel(filename, index_col=0)
    print(a.head())


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


@app.route('/upload', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = form.name.data + '.csv'
        f.save(os.path.join(
            filename
        ))

        df = pd.read_csv(f, header=None)
        print(df.head())

        return "AAA"

    return render_template('upload.html', form=form)


'''
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
           # filename = secure_filename(file.filename )
           # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            a = pd.read_excel('a.xls', index_col=0)
           # print(a.head())
            return render_template("result.html")

    return render_template("upload.html")


    '''
if __name__ == '__main__':
    app.run()