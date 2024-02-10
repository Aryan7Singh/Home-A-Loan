# dependencies
import csv
import os
from flask import Flask, redirect, render_template, request
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def landing_page():
    return redirect('/home')

@app.route('/home')
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()