import json
from flask import request
from flask_restful import Resource
import pandas as pd
import gc


class Processing(Resource):
    def post(self):
        req = request.get_json(silent=True)
        df = pd.json_normalize(req, record_path=['items'])

        df['createdAt'] = pd.to_datetime(df['createdAt'], unit='s')
        df.set_index('createdAt', inplace=True)

        tmp = df.resample('1min').mean().interpolate()
        resampled = tmp.resample('1H').ffill()
        resampled.reset_index(inplace=True)
        resampled['createdAt'] = resampled['createdAt'].astype(int) / 10**9
        resampled['createdAt'] = resampled['createdAt'].astype(int)
        resampled = resampled.iloc[1:, :]

        print(resampled)

        resp = json.loads(resampled.to_json(orient='records'))
        del [[df, tmp, resampled]]
        gc.collect()
        return resp
