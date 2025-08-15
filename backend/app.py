from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from backend.prediction import predict_copd_severity
import json
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')
CORS(app, 
     supports_credentials=True,
     resources={
         r"/*": {
             "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type"],
             "supports_credentials": True
         }
     })

# Set session cookie settings
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# User database (JSON file)
USER_DB_FILE = 'users.json'
PREDICTIONS_FILE = 'predictions.json'
PATIENTS_FILE = 'patients.json'

def init_db():
    if not os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(PREDICTIONS_FILE):
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(PATIENTS_FILE):
        with open(PATIENTS_FILE, 'w') as f:
            json.dump([], f)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Session contents:", session)  # Debug print
        if 'username' not in session:
            print("User not in session, redirecting to login")  # Debug print
            return redirect(url_for('login'))
        print(f"User {session['username']} is authenticated")  # Debug print
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        with open(USER_DB_FILE, 'r') as f:
            users = json.load(f)
            
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        with open(USER_DB_FILE, 'r') as f:
            users = json.load(f)
            
        if username in users:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
            
        users[username] = {
            'password': password,
            'created_at': datetime.now().isoformat()
        }
        
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users, f)
            
        return jsonify({'success': True})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    with open(PREDICTIONS_FILE, 'r') as f:
        predictions = json.load(f)
    with open(PATIENTS_FILE, 'r') as f:
        patients = json.load(f)
    
    # Filter predictions for current user
    recent_predictions = [p for p in predictions if p['username'] == session['username']][-5:]
    
    # Filter patients for current user
    user_patients = [p for p in patients if p['username'] == session['username']]
    
    return render_template('dashboard.html', 
                         predictions=recent_predictions,
                         patients=user_patients)

@app.route('/add-patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        data = request.json
        required_fields = ['name', 'age', 'gender']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
            
        new_patient = {
            'id': str(len(get_patients()) + 1),
            'username': session['username'],
            'name': data['name'],
            'age': data['age'],
            'gender': data['gender'],
            'created_at': datetime.now().isoformat(),
            'last_visit': None
        }
        
        patients = get_patients()
        patients.append(new_patient)
        
        with open(PATIENTS_FILE, 'w') as f:
            json.dump(patients, f)
            
        return jsonify({'success': True, 'patient': new_patient})
    
    return render_template('add-patient.html')

@app.route('/patient/<patient_id>/predictions')
@login_required
def patient_predictions(patient_id):
    with open(PREDICTIONS_FILE, 'r') as f:
        predictions = json.load(f)
    with open(PATIENTS_FILE, 'r') as f:
        patients = json.load(f)
    
    # Find patient
    patient = next((p for p in patients if p['id'] == patient_id and p['username'] == session['username']), None)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Get patient's predictions
    patient_predictions = [p for p in predictions if p.get('patient_id') == patient_id]
    
    return render_template('patient-predictions.html', 
                         patient=patient,
                         predictions=patient_predictions)

def get_patients():
    with open(PATIENTS_FILE, 'r') as f:
        return json.load(f)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        
        # Validate required fields
        required_fields = ['AGE', 'PackHistory', 'MWT1Best', 'FEV1', 'FEV1PRED', 'FVC', 'FVCPRED', 
                          'CAT', 'HAD', 'SGRQ', 'AGEquartiles', 'gender', 'smoking', 'Diabetes', 
                          'muscular', 'hypertension', 'AtrialFib', 'IHD']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(f"Missing required fields: {missing_fields}")  # Debug print
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
            
        severity, probabilities = predict_copd_severity(data)
        
        # Save prediction
        prediction_data = {
            'username': session['username'],
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'probabilities': probabilities,
            'input_data': data
        }
        
        with open(PREDICTIONS_FILE, 'r') as f:
            predictions = json.load(f)
        
        predictions.append(prediction_data)
        
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(predictions, f)
        
        return jsonify({
            'severity': severity,
            'probabilities': probabilities
        })
    except Exception as e:
        print(f"Error in predict endpoint: {str(e)}")  # Debug print
        import traceback
        print(traceback.format_exc())  # Print full traceback
        return jsonify({'error': str(e)}), 400

@app.route('/prediction-form')
@login_required
def prediction_form():
    return render_template('prediction-form.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000) 
