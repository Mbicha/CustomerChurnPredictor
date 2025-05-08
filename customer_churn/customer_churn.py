from flask import Flask, request, jsonify, render_template
import json
import os

from db.database import insert_document
app = Flask(__name__)

static_folder = os.path.join(app.root_path, 'static')


# Categorical Mappings
categorical_mappings = {
    "online_security": {"No": 0, "No internet service": 1, "Yes": 2},
    "online_backup": {"No": 0, "No internet service": 1, "Yes": 2},
    "tech_support": {"No": 0, "No internet service": 1, "Yes": 2},
    "contract": {"Month-to-month": 0, "One year": 1, "Two year": 2}
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/survey/<filename>')
def takeSurvey(filename):
    SLNO = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
    survey_data = getSurveyQuiz()
    return render_template(filename, slno=SLNO, size=len(survey_data['survey']) , survey_data = survey_data)

@app.route('/predict_churn', methods=['POST'])
def predictChurn():
    try:
        form_data = {}
        features = ["teunure", "online_security", "online_backup", "tech_support", "contract", "total_charges", "monthly_charges"]
        for feature in features:
            form_data[feature] = request.form[feature]
        
        # Convert categorical features to their encoded values
        processed_data = []
        for feature in features:
            if feature in categorical_mappings:  # Categorical feature
                value = form_data[feature]
                if value not in categorical_mappings[feature]:
                    return jsonify({"error": f"Invalid value '{value}' for {feature}"})
                processed_data.append(int(categorical_mappings[feature][value]))
            else:  # Numerical feature (tenure, total_charges, monthly_charges)
                processed_data.append(float(form_data[feature]))  # Convert to float

        # Example: Print processed data (replace with your model prediction)
        print("Processed data:", processed_data)

        # Placeholder for prediction logic (e.g., using a machine learning model)
        # prediction = your_model.predict([processed_data])
        # prediction = "No churn"  # Dummy response
        
        # return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})



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