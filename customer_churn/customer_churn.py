from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey/<filename>')
def takeSurvey(filename):
    return render_template(filename)

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     prediction = model.predict(data)
#     return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)