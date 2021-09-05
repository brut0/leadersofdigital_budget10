import flask
from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file,redirect,Response
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#from pylab import *
from model import BudgetModel
import os
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
#from bokeh.io import output_file
#from bokeh.plotting import figure, show

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/')
def index():
    return render_template("first.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/result')
def info():
    return render_template("result.html")


#helper - function for building model
def build_model():
    try:
        X = pd.read_csv('features.csv', index_col=0)
        y = pd.read_csv('target.csv', index_col=0)
        print('All of the data has been loaded successfully!')
    except Exception as err:
        print(repr(err))
    print()

    tmp = BudgetModel(X, y)
    tmp.train()
    predicts = tmp.predict()
    for i, p in enumerate(predicts):
        print(i)
        p.to_csv('predict', index=False)
    return predicts


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == "POST":
        #upload two files
        uploaded_files = flask.request.files.getlist("file[]")
        print (uploaded_files)
        #check that files are read
        for f in uploaded_files:
            df = pd.read_excel(f, index_col=0)
            print(df.head())
        #for example lets assume we got correct input features.csv and target.csv
        predict = build_model()
        print(predict)
        filename = 'predict'
        return send_file(filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)
        print(predict)


    else:
        return render_template('upload.html')



TARGET = 'Налог на доходы физических лиц'
SEED = 42
FIGSIZE = (12,5)
FONTSIZE = 14
YEARS_PREDICT = 2

#make graphic
#do later
def make_plot(df_predict,y=2,X=[]):
    width = 0.4  # the width of the bars
    xt = np.arange(len(X.index))

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(xt, y.iloc[:, 0])
    ax.scatter(xt, y.iloc[:, 0])
    for i in range(df_predict.shape[0]):
        ax.plot(xt[-YEARS_PREDICT:], df_predict.loc[i, 'predicted'])
        ax.scatter(xt[-YEARS_PREDICT:], df_predict.loc[i, 'predicted'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('руб', fontsize=FONTSIZE + 2)
    ax.set_xlabel('год', fontsize=FONTSIZE + 2)

    ax.set_title(TARGET, fontsize=FONTSIZE + 4)
    ax.set_xticks(xt)
    ax.set_xticklabels([str(y) for y in X.index], fontsize=FONTSIZE)
    l = [f'Прогноз {model}' for model in df_predict['model_name']]
    legend1 = ax.legend(['Реальные данные', *l])
    ax.add_artist(legend1)

    fig.tight_layout()

    plt.show()



if __name__ == '__main__':
    app.run(host='172.18.0.2', port=5000, debug=True)
