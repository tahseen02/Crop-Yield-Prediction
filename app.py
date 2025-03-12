from flask import Flask,request, render_template
import numpy as np
import pickle
import sklearn
from flask import Flask, render_template, request,redirect,url_for,flash, session
import pickle
import random
import os
import pandas as pd
import random
import string

print(sklearn.__version__)


#flask app
app = Flask(__name__)

def generate_secret_key(length=24):
    """Generate a random string to be used as the Flask app secret key."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Set secret key for session management
app.secret_key = generate_secret_key()


#loading models
dtr = pickle.load(open('dtr.pkl','rb'))
preprocessor = pickle.load(open('preprocessor.pkl','rb'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
    
    return render_template('login.html')


@app.route('/')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')



@app.route("/predict",methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = request.form['Year']
        average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
        pesticides_tonnes = request.form['pesticides_tonnes']
        avg_temp = request.form['avg_temp']
        Area = request.form['Area']
        Item  = request.form['Item']

        features = np.array([[Year,average_rain_fall_mm_per_year,pesticides_tonnes,avg_temp,Area,Item]],dtype=object)
        transformed_features = preprocessor.transform(features)
        prediction = dtr.predict(transformed_features).reshape(1,-1)

        return render_template('index.html',prediction = prediction[0][0])

if __name__=="__main__":
    app.run(debug=True)