from flask import Flask, request, jsonify, render_template
import json
import os

from db.database import insert_document
app = Flask(__name__)

static_folder = os.path.join(app.root_path, 'static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/survey/<filename>')
def takeSurvey(filename):
    SLNO = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
    survey_data = getSurveyQuiz()
    return render_template(filename, slno=SLNO, size=len(survey_data['survey']) , survey_data = survey_data)


@app.route('/submit_survey', methods=['POST'])
def submitSurvey():
    survey_data = {}
    try:
        for key in request.form:
            survey_data[key] = request.form[key]
        response = insert_document(survey_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

def getSurveyQuiz():
    json_path = os.path.join(static_folder, 'Assets', 'survey_quiz.json')
    with open(json_path) as f:
        survey_data = json.load(f)
    return survey_data

if __name__ == '__main__':
    app.run(debug=True)
