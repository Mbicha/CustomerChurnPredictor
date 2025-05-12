from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import numpy as np
import joblib
import json
import os

from db.database import insert_document
app = Flask(__name__)
app.secret_key = 'ChurnPredictionApp'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'churn_'

static_folder = os.path.join(app.root_path, 'static')
# Load your model (adjust the path as needed)
try:
    model = joblib.load('customer_churn/churn.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

#  Load label.json file
categorical_mappings = {}
with open(os.path.join(static_folder, 'Assets', 'labels.json')) as f:
    categorical_mappings = json.load(f)

def convert_request_values(request_data, labels):
    converted_data = {}
    
    for key, value in request_data.items():
        # Handle numeric fields
        if key in ['tenure']:  # Integer fields
            try:
                converted_data[key] = int(float(value))  # Convert to float first to handle "123.0" cases
            except (ValueError, TypeError):
                raise ValueError(f"Invalid integer value for {key}: {value}")
        
        elif key in ['total_charges', 'monthly_charges']:  # Float fields
            try:
                converted_data[key] = float(value)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid float value for {key}: {value}")
        
        # Handle categorical fields using labels mapping
        elif key in labels:
            # Normalize the key (some labels might have different capitalization)
            normalized_key = next((k for k in labels.keys() if k.lower() == key.lower()), key)
            
            if normalized_key in labels:
                if value in labels[normalized_key]:
                    converted_data[key] = labels[normalized_key][value]
                else:
                    raise ValueError(f"Invalid value '{value}' for {key}. Allowed values: {list(labels[normalized_key].keys())}")
            else:
                raise ValueError(f"No label mapping found for {key}")
        
        # Handle case where field isn't in labels and isn't a known numeric field
        else:
            converted_data[key] = value  # keep as-is if not a field we need to convert
    
    return converted_data

def prepare_data_for_prediction(data):
    """
    Prepare the processed data for model prediction by converting to correct format.
    Returns a numpy array in the shape expected by the model.
    """
    # Define the expected feature order (adjust according to your model)
    feature_order = [
        'tenure',
        'online_security',
        'online_backup',
        'tech_support',
        'contract',
        'monthly_charges',
        'total_charges'
    ]
    
    # Convert the dictionary to a list in the correct order
    return np.array([[data[feature] for feature in feature_order]])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    prediction_results = session.get('prediction_results')
    print("Prediction results from session:", prediction_results)
    if not prediction_results:
        return redirect(url_for('index'))
    return render_template('results.html',
                         prediction=prediction_results['prediction'],
                         probability=prediction_results['probability'],
                         processed_data=prediction_results['processed_data'])

@app.route('/survey/<filename>')
def takeSurvey(filename):
    SLNO = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
    survey_data = getSurveyQuiz()
    return render_template(filename, slno=SLNO, size=len(survey_data['survey']) , survey_data = survey_data)

@app.route('/predict_churn/results', methods=['POST'])
def predictChurn():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        if request.method != 'POST':
            return jsonify({"error": "Method not allowed"}), 405

        # List of expected features
        features = [
            "tenure", 
            "online_security", 
            "online_backup", 
            "tech_support", 
            "contract", 
            "total_charges", 
            "monthly_charges"
        ]

        # Verify all required fields are present
        missing_fields = [f for f in features if f not in request.form]
        if missing_fields:
            return jsonify({"error": f"Missing features: {', '.join(missing_fields)}"}), 400

        # Extract form data
        form_data = {feature: request.form[feature] for feature in features}
        
        # Convert values to appropriate types
        processed_data = convert_request_values(form_data, categorical_mappings)
        print("Processed data:", processed_data)

        # Prepare data for prediction
        prediction_data = prepare_data_for_prediction(processed_data)
        print("Data for prediction:", prediction_data)

        # Make prediction
        prediction = model.predict(prediction_data)
        prediction_proba = model.predict_proba(prediction_data) if hasattr(model, 'predict_proba') else None

        # Prepare response
        # response = {
        #     "prediction": int(prediction[0]),  # Convert numpy int to Python int
        #     "processed_data": processed_data
        # }

        # # Add probabilities if available
        # if prediction_proba is not None:
        #     response["probability"] = {
        #         "no_churn": float(prediction_proba[0][0]),
        #         "churn": float(prediction_proba[0][1])
        #     }
        session['prediction_results'] = {
            "prediction": int(prediction[0]),
            "probability": {
                "no_churn": float(prediction_proba[0][0]),
                "churn": float(prediction_proba[0][1])
            },
            "processed_data": processed_data
        }

        return redirect(url_for('results'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

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