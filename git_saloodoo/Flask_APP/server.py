from flask import Flask
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
import pickle
import json

import preprocess_file
import label_encoder

import train_model

app = Flask(__name__)

@app.route('/')
def firstfile():
	print("root page")
	return 'root page'

@app.route('/train_model_api')
def train_model_fun():
    train_model.model_build()
    return 'model_train is done'

@app.route('/predict',methods=['POST'])
def predict_func():
	print("hello")
	test_json_dump = json.dumps(request.get_json())

	test_df = pd.read_json(test_json_dump, orient='index')
	print(test_df)
	filename = 'finalized_model.pkl'
	model =  pickle.load(open(filename, 'rb'))
	
	preprocess_step = Pipeline(steps=[('preprocess',preprocess_file.Indego()),('label',label_encoder.custom_label_encoder())])
	dataset = preprocess_step.fit_transform(test_df.T) 
	predicted_data = model.predict(dataset)

	print(predicted_data[0])
	return jsonify({"duration":np.expm1(predicted_data[0])})
	


if __name__ == "__main__":
    app.run()