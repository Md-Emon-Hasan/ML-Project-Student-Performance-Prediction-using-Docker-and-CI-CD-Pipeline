from flask import Flask
from flask import request
from flask import render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData
from src.pipeline.predict_pipeline import PredictPipeline

application = Flask(__name__)
app = application

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'POST':
        # Extract form data
        gender = request.form.get('gender')
        race_ethnicity = request.form.get('ethnicity')
        parental_level_of_education = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_preparation_course = request.form.get('test_preparation_course')
        reading_score = float(request.form.get('reading_score'))
        writing_score = float(request.form.get('writing_score'))

        # Prepare data for prediction
        data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )
        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        print("Before Prediction")
        predict_pipeline = PredictPipeline()
        results = f"{predict_pipeline.predict(pred_df)[0]:.2f}"
        print("After Prediction")

        # Pass form data and result to the template
        return render_template(
            'index.html',
            results=results,
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )
    else:
        # If GET request, render the template without pre-filled values
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
