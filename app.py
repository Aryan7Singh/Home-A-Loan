# dependencies
import csv
import os
from flask import Flask, redirect, render_template, request
import pandas as pd 

app = Flask(__name__)

# Load pickle model 

def load_model():
    import pickle
    global model
    model = pickle.load(open('model.pkl', 'rb'))
        

@app.route('/')
def landing_page():
    return redirect('/home')

@app.route('/home')
def home_page():
    return render_template("index.html")

@app.route('/index.html')
def reLandingPage():
    return redirect('/home')

@app.route('/prediction', methods=['POST'])
def prediction():
    load_model()
    
if __name__ == "__main__":
    app.run()