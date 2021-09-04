from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file
from sklearn.externals import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

knn = joblib.load('knn.pkl')


@app.route('/')
def hello_world():
    return '<h1>Hello, my very best friend!!!!!!!</h1>'

@app.route('/iris/<param>')
def iris(param):
    param = param.split(',')
    param = [float(num) for num in param]

    param = np.array(param).reshape(1, -1)
    predict = knn.predict(param)

    return str(predict)

@app.route('/iris_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()

        param = content['flower'].split(',')
        param = [float(num) for num in param]

        param = np.array(param).reshape(1, -1)
        predict = knn.predict(param)

        predict = {'class': str(predict[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predict)


from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()


from werkzeug.utils import secure_filename
import os


@app.route('/upload', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = form.name.data + '.csv'
        # f.save(os.path.join(
        #     filename
        # ))

        df = pd.read_csv(f, header=None)
        print(df.head())
        '''
        predict = knn.predict(df)

        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False)
        '''
        return "A"

        return send_file(filename,
                         mimetype='text/csv',
                         attachment_filename=filename,
                         as_attachment=True)

    return render_template('upload.html', form=form)


import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


