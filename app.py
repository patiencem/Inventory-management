from datetime import date
from fileinput import filename
from msilib.schema import File
from unittest import result
from flask import Flask, render_template, request, redirect, url_for, make_response
import os
from os.path import join, dirname, realpath
import io
import csv
from statsmodels.tsa.statespace.sarimax import SARIMAX
from io import StringIO
import pickle
import pandas as pd
import numpy as np

app= Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/')
def hello_world():
    return render_template("login.html")
database={'admin':'admin'}


@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
        return render_template('login.html', info='invalid User')
    else:
            if database[name1]!=pwd:
                return render_template('login.html',info='invalid Password')
            else:
                    return redirect(url_for('index.html'))

app.config["DEBUG"] = True

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():

    return render_template('index.html')

@app.route("/", methods=['POST'])
def upload_files():
    data=[]
    uploaded_file =request.files['file']
    if uploaded_file.filename !='':
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        with open(file_path) as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row)
    return redirect(url_for('index'))

app.config['UPLOAD_FOLDER'] = "C:\\Users\\Patience\FINAL\\static"


def parseCSV(filePath):
    col_names = ['drugName','year','week','total_weekly_stock','min_week_date']
    csvData = pd.read_csv(filePath,names=col_names, header=None)
    for i, row in csvData.iterrows():
        print(i,row['drugName'],row['year'],row['week'],row['total_weekly_stock'],row['min_week_date'],)


def SARIMAX_model(stock_vals,forecast_len,param_1):
    """
    Forecast using SARIMAX model
    """
    
    SARIMAX_model= SARIMAX(stock_vals, exog=None, order=(1, 1,3), seasonal_order=(1, 1,1,param_1)
                             ).fit(dis=-1)
    forecast_vals_SARIMAX=SARIMAX_model.get_forecast(steps=forecast_len)
    predicted=forecast_vals_SARIMAX.summary_frame()["mean"].values
    return predicted



@app.route('/predict',methods=['POST', 'GET'])
def predict():
    filename = 'C:/Users/Patience/Documents/try.csv' 
 
	# to read the csv file using the pandas library 
    data = pd.read_csv(filename, header=0) 
    myData = data.values
    prediction = SARIMAX_model(myData, 6, 6)

    
    
    return render_template('index.html', prediction_text='Predicted Stock for the next six months: {}'.format(prediction))
    

if (__name__=="__main__"):
      app.run(port = 5000)

    













