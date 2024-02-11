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
    slider_values = data.get('sliderValues', {})
    birth_year = int(slider_values.get('yearOfBirth', 0))
    averageDaysPastDue = int(slider_values.get('averageDaysPastDue', 0))
    totalLoanPayments = int(slider_values.get('totalLoanPayments', 0))
    numberofInstallments = int(slider_values.get('numberofInstallments', 0))
    percentageofLateInstallment = float(slider_values.get('percentageofLateInstallment', 0)) / 100
    interestRate = float(slider_values.get('interestRate', 0)) / 100
    selected_models = data.get('selectedModels', [])
    model = Model(selected_models)
    return jsonify({'message': "Risk: " + "{:.2f}".format(model.predict(birth_year, averageDaysPastDue, totalLoanPayments, numberofInstallments, percentageofLateInstallment, interestRate) * 100) + "%"})


@app.route('/insights', methods=['POST'])
def insights():
    return render_template('insights.html')
@app.route('/back', methods=['POST'])
def go_back():
    return render_template('index.html')

class Model:
    def __init__(self, dirs):
        self.models = [SingleModel(dir) for dir in dirs]

    def predict(self, birth_year=None, avg_dpd=None, pay_count=None,
                num_early_inst=None, perc_late_inst=None,
                interest=None):
        out = 0
        for model in self.models:
            out += model.predict(birth_year=birth_year, avg_dpd=avg_dpd, pay_count=pay_count,
                                 num_early_inst=num_early_inst, perc_late_inst=perc_late_inst,
                                 interest=interest)
        out /= len(self.models)
        return out


class SingleModel:
    def __init__(self, dir="lgb"):
        dir_files = [f"{dir}/{file}" for file in os.listdir(dir)]
        imp_path = f"{dir}/imp.pkl"
        self.imp = None
        if imp_path in dir_files:
            self.imp = joblib.load(imp_path)
        self.scaler = joblib.load(f"{dir}/scaler.pkl")
        self.models = []
        for file in dir_files:
            if file.endswith("model.pkl"):
                self.models.append(joblib.load(file))
        self.input = pd.read_parquet(dir + "/example.parquet")
        self.input.loc[:] = np.nan

    # ==============VARIABLE DESCRIPTIONS===============
    # birth_year: birth year
    # avg_dpd: Average DPD (days past due) with tolerance within the past 24 months from the maximum closure date, assuming that the contract is finished. If the contract is ongoing, the calculation is based on the current date.
    # pay_count: Total number of loan payments made by the client.
    # num_early_inst: Number of instalments paid more than three days before the due date.
    # perc_late_inst: Percentage of installments that are paid 1 or more days after the due date.
    # interest: interest rate
    # ===============VARIABLE RANGES====================
    # birth_year: [1960, 2000]
    # avg_dpd: [0, 10]
    # pay_count: [0, 60]
    # num_early_inst: [0, 60]
    # perc_late_inst: [0, 1]
    # interest: [0, 0.40]
    def predict(self, birth_year=None, avg_dpd=None, pay_count=None,
                num_early_inst=None, perc_late_inst=None,
                interest=None):
        curr_input = deepcopy(self.input)
        if self.imp is not None:
            curr_input[:] = self.imp.transform(curr_input)
        if birth_year is not None:
            birth_date = (datetime(birth_year, 1, 1) - datetime(1900, 1, 1)).days
            for column in curr_input.columns:
                if column.startswith("birthdate") or column.startswith("dateofbirth"):
                    curr_input.loc[0, column] = birth_date
        if avg_dpd is not None:
            curr_input.loc[0, "avgdpdtolclosure24_3658938P"] = avg_dpd
        if pay_count is not None:
            curr_input.loc[0, "pmtnum_254L"] = pay_count
        if num_early_inst is not None:
            curr_input.loc[0, "numinstpaidearly3d_3546850L"] = num_early_inst
        if perc_late_inst is not None:
            curr_input.loc[0, "pctinstlsallpaidlate1d_3546856L"] = perc_late_inst
        if interest is not None:
            curr_input.loc[0, "eir_270L"] = interest
        curr_input[:] = self.scaler.transform(curr_input)
        out = 0
        for model in self.models:
            # print(model.coef_[0])
            out += float(model.predict_proba(curr_input)[0, 1])
        out /= len(self.models)
        return out






if __name__ == "__main__":
    app.run()
