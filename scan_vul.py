from flask import Flask, request, jsonify
import os
import re
from flask_cors import CORS

app = Flask(__name__)

# Allow requests from localhost:8000 (your frontend)
CORS(app, origins="http://localhost:8000", supports_credentials=True)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_request
def log_request_info():
    print(f"Request Headers: {request.headers}")
    print(f"Request Data: {request.form}")

# Basic scanner for SQL Injection, XSS, and CSRF
def scan_for_vulnerability(file_path, vulnerability_type):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        result = {
            'file': file_path,
            'vulnerability': vulnerability_type,
            'status': 'scan completed',
            'issues_found': []
        }

        # SQL Injection Detection
        if vulnerability_type == 'sql_injection':
            if re.search(r"(UNION\s+SELECT|OR\s+1=1|SELECT\s+\*|DROP\s+TABLE|--)", content, re.IGNORECASE):
                result['issues_found'].append("Potential SQL Injection vulnerability detected.")
        
        # Cross-Site Scripting (XSS) Detection
        elif vulnerability_type == 'xss':
            if re.search(r"(<script.*?>.*?</script>|on\w*=\s*['\"]*.*?['\"]*)", content, re.IGNORECASE):
                result['issues_found'].append("Possible Cross-Site Scripting (XSS) vulnerability detected.")
        
        # Cross-Site Request Forgery (CSRF) Detection
        elif vulnerability_type == 'csrf':
            if re.search(r'<form.*?>.*?</form>', content, re.IGNORECASE):
                if not re.search(r'csrf_token', content, re.IGNORECASE):
                    result['issues_found'].append("CSRF token missing in form.")

        if not result['issues_found']:
            result['issues_found'].append("No issues detected.")
        
        return result
    except Exception as e:
        return {'error': f'Error while scanning file: {str(e)}'}

@app.route('/scan-vulnerability', methods=['POST'])
def scan_vulnerability():
    try:
        # Check if the file is present in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Get the selected vulnerability type
        vulnerability_type = request.form.get('vulnerability')

        # Call the scan function
        scan_result = scan_for_vulnerability(file_path, vulnerability_type)

        if 'error' in scan_result:
            return jsonify(scan_result), 500

        return jsonify(scan_result)

    except Exception as e:
        return jsonify({'error': f'Error during scan: {str(e)}'}), 500

if __name__ == '__main__':
    # Ensure the uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True, host='0.0.0.0', port=5001)  # Run Flask app on port 5001
