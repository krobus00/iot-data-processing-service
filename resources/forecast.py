import json
from flask import request
from flask_restful import Resource
import pandas as pd
import gc
import pickle
from urllib.request import urlopen


class Forecast(Resource):
    def post(self):
        req = request.get_json(silent=True)
        model = req['model']

        df = pd.json_normalize(req, record_path=['items'])
        df['createdAt'] = pd.to_datetime(df['createdAt'], unit='s')
        df.set_index('createdAt', inplace=True)
        df = df.resample('1h').mean().interpolate()
        df.reset_index(inplace=True)
        df = df[['createdAt', 'temperature']]
        df.columns = ['ds', 'y']

        m = pickle.load(urlopen(model))
        future = m.make_future_dataframe(
            df,
            periods=25,
        )
        forecast = m.predict(future)
        df = forecast[['ds', 'yhat1']]
        df['ds'] = df['ds'].astype(int) / 10**9
        df['ds'] = df['ds'].astype(int)
        resp = json.loads(df.to_json(orient='records'))
        del [[df]]
        gc.collect()
        return resp
