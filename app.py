from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS issues
import joblib  # For loading models
import re  # For URL preprocessing

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the front-end origin (http://localhost:8000)
CORS(app, resources={r"/predict": {"origins": "http://localhost:8000"}})

# Load the model and vectorizer
model = joblib.load('url_classifier_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Preprocess the URL function (same as in training)
def preprocess_url(url):
    # Remove special characters and tokenize
    url = re.sub(r'\W+', ' ', url)
    return url.lower()

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get URL from the POST request
        data = request.get_json()
        url = data['url']

        # Preprocess the URL
        processed_url = preprocess_url(url)

        # Vectorize the preprocessed URL
        url_vectorized = vectorizer.transform([processed_url])

        # Make the prediction using the loaded model
        prediction = model.predict(url_vectorized)

        # Map prediction to 'Malicious' or 'Safe'
        result = {'prediction': 'Malicious' if prediction[0] == 1 else 'Safe'}

        # Return prediction as JSON response
        return jsonify(result)

    except Exception as e:
        # Handle errors and return a meaningful response
        return jsonify({'error': str(e)}), 500

# Main route
if __name__ == '__main__':
    app.run(debug=True)
