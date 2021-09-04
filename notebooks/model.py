import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from catboost import CatBoostRegressor
from catboost import Pool
import shap as shap


class BudgetModel():
    def __init__(self, X, y, random_seed=42):
        self.SEED = random_seed
        self.YEARS_PREDICT = 2
        self.X_train, self.X_test = 0, 0
        self.y_train, self.y_test = 0, 0

        self.X = X
        self.y = y

    def train(self):
        self.X_train, self.X_test = self.X[:-self.YEARS_PREDICT], self.X[-self.YEARS_PREDICT:]
        self.y_train, self.y_test = self.y[:-self.YEARS_PREDICT], self.y[-self.YEARS_PREDICT:]

        self.X_train = self.X_train.fillna(0)
        self.X_test = self.X_test.fillna(0)

    def predict(self):
        # def linear_fit(X_train=None, y_train=None, target=None):
        #     model = LinearRegression()
        #     result = model.fit(X_train, y_train[target])
        #     return result
        #
        # def catboost_fit(X_train=None, y_train=None, target=None):
        #     model = CatBoostRegressor(**catboost_params)
        #     result = model.fit(X_train, y_train[target])
        #     return result
        #
        # def arima_fit(X_train=None, y_train=None, target=None):
        #     model = ARIMA(y_train[target], order=(3, 2, 1))
        #     result = model.fit()
        #     return result

        catboost_params = {
            'depth': 6,
            # 'l2_leaf_reg': 10,
            'iterations': 30000,
            'learning_rate': 0.1,
            'eval_metric': 'MAE',
            'early_stopping_rounds': 50,
            'verbose': 5000,
            'thread_count': 4,
            'random_seed': self.SEED
        }

        # models = {
        #     'Linear': linear_fit(),
        #     'ARIMA': arima_fit(),
        #     'CatBoost': arima_fit()
        # }

        dfs = []

        for target in self.y.columns[1:]:
            df_predict = pd.DataFrame({'year': self.y.index[-2:]})

            model = LinearRegression()
            model.fit(self.X_train, self.y_train[target])
            predicted = model.predict(self.X_test)
            df_predict['Linear'] = predicted

            # model = CatBoostRegressor(**catboost_params)
            # model.fit(self.X_train, self.y_train[target])
            # predicted = model.predict(self.X_test)
            # df_predict = df_predict.append({'model_name': 'CatBoost', 'model': model, 'predicted': predicted}, ignore_index=True)

            model = ARIMA(self.y_train[target], order=(3, 2, 1))
            arima_result = model.fit()
            predicted = arima_result.predict(start=len(self.y_train), end=len(self.y) - 1)
            df_predict['ARIMA'] = predicted

            dfs.append(df_predict)

        return dfs