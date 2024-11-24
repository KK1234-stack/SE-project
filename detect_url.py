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

# Hardcoded good and bad websites
hardcoded_good_urls = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://www.wikipedia.org"
]

hardcoded_bad_urls = [
    "http://malicious-site.com",
    "http://phishing-site.com",
    "http://fake-bank.com",
    "http://dangerous-link.com",
    "http://spammy-site.com"
]

# Preprocess the URL function (same as in training)
def preprocess_url(url):
    # Remove special characters and tokenize
    url = re.sub(r'\W+', ' ', url)
    return url.lower()

# Function to classify a URL using hardcoded values first
def classify_url(url):
    if url in hardcoded_good_urls:
        return "Safe (Hardcoded)"
    elif url in hardcoded_bad_urls:
        return "Malicious (Hardcoded)"
    else:
        # If not hardcoded, use the trained model for prediction
        url_vectorized = vectorizer.transform([url])
        prediction = model.predict(url_vectorized)
        return "Malicious" if prediction == 1 else "Safe"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get URL from the POST request
        data = request.get_json()
        url = data['url']

        # Preprocess the URL
        processed_url = preprocess_url(url)

        # Classify using hardcoded values first
        classification = classify_url(processed_url)

        # Return prediction as JSON response
        return jsonify({'prediction': classification})

    except Exception as e:
        # Handle errors and return a meaningful response
        return jsonify({'error': str(e)}), 500

# Main route
if __name__ == '__main__':
    app.run(debug=True)
