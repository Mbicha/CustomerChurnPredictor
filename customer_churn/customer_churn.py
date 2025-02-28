from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

static_folder = os.path.join(app.root_path, 'static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/survey/<filename>')
def takeSurvey(filename):
    survey_data = getSurveyQuiz()
    return render_template(filename, slno="Q", size=len(survey_data['survey']) , survey_data = survey_data)


def getSurveyQuiz():
    json_path = os.path.join(static_folder, 'Assets', 'survey_quiz.json')
    with open(json_path) as f:
        survey_data = json.load(f)
        # for item in survey_data['survey']:
        #     # Print the question first
        #     print(item['question'])
        #     # Then print each answer
        #     for answer in item['answers']:
        #         print(answer)
        #     # Add a blank line between questions for clarity
        #     print("")
    return survey_data

if __name__ == '__main__':
    app.run(debug=True)
