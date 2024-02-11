from flask import Flask, redirect, render_template, request, jsonify
import joblib
import os, glob
import gc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Literal
import polars as pl
import polars.selectors as cs
from sklearn.model_selection import train_test_split, cross_validate, StratifiedGroupKFold
from sklearn.metrics import roc_auc_score
from datetime import datetime
from copy import deepcopy

import lightgbm as lgb
from tqdm import tqdm

app = Flask(__name__)

@app.route('/')
def landing_page():
    return redirect('/home')

@app.route('/home')
def home_page():
    return render_template("index.html")

@app.route('/prediction', methods=['POST'])
def prediction():
    data = request.get_json()
    birth_year = int(data.get('yearOfBirth', 0))
    debt = int(data.get('debt', 0))
    for slider_name, slider_value in data.items():
        print(f"Slider '{slider_name}' value: {slider_value}")
    model = Model()
    print(model.predict(birth_year, debt))
    return jsonify({'message': 'Slider values received successfully'})



class Model:
    def __init__(self, dir="saved_models"):
        dir_files = [f"{dir}/{file}" for file in os.listdir(dir)]
        self.models = []
        for file in dir_files:
            if file.endswith(".pkl"):
                self.models.append(joblib.load(file))
        self.input = pd.read_parquet(dir + "/example.parquet")
        self.input.loc[:] = np.nan

    def predict(self, birth_year, debt):
        birth_date = (datetime(birth_year, 1, 1) - datetime(1900, 1, 1)).days
        for column in self.input.columns:
            if column.startswith("birthdate") or column.startswith("dateofbirth"):
                self.input.loc[0, column] = birth_date
        self.input.loc[0, "totaldebt_9A"] = debt
        out = 0
        for model in self.models:
            out += float(model.predict_proba(self.input)[0, 1])
        out /= len(self.models)
        self.input.loc[:] = np.nan
        return out


if __name__ == "__main__":
    app.run()
