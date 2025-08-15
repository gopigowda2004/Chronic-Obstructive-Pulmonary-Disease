import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# Step 1: Load and Preprocess the Full Dataset
df = pd.read_csv('/home/thekingcb/Documents/MyProjects/project 5/dev/model/dataset.csv')
df.replace('NA', np.nan, inplace=True)
for col in ['MWT1', 'MWT2', 'MWT1Best']:
    df[col] = df[col].fillna(df[col].median())
df = df.drop(['Unnamed: 0', 'ID', 'copd', 'MWT1', 'MWT2'], axis=1)

# Encode target
le = LabelEncoder()
df['COPDSEVERITY'] = le.fit_transform(df['COPDSEVERITY'])
severity_classes = le.classes_  # ['MILD', 'MODERATE', 'SEVERE', 'VERY SEVERE']

# Scale features
numeric_cols = [col for col in df.columns if col != 'COPDSEVERITY']
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Features and target
X = df.drop('COPDSEVERITY', axis=1)
y = df['COPDSEVERITY']

# Step 2: Train Final Model on Full Data
rf_final = RandomForestClassifier(n_estimators=100, random_state=42)
rf_final.fit(X, y)

# Step 3: Save Model and Preprocessing Objects
joblib.dump(rf_final, 'copd_rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(le, 'label_encoder.pkl')
print("Model and preprocessing objects saved as 'copd_rf_model.pkl', 'scaler.pkl', and 'label_encoder.pkl'")

# Step 4: Prediction Function for New Data
def predict_copd_severity(new_data, model_path='copd_rf_model.pkl', scaler_path='scaler.pkl', le_path='label_encoder.pkl'):
    """
    Predict COPD severity for new patient data.
    
    Parameters:
    - new_data: Dict or DataFrame with 18 features in order: 
      ['AGE', 'PackHistory', 'MWT1Best', 'FEV1', 'FEV1PRED', 'FVC', 'FVCPRED', 
       'CAT', 'HAD', 'SGRQ', 'AGEquartiles', 'gender', 'smoking', 'Diabetes', 
       'muscular', 'hypertension', 'AtrialFib', 'IHD']
    
    Returns:
    - Predicted severity (string: 'MILD', 'MODERATE', 'SEVERE', 'VERY SEVERE')
    """
    # Load model and preprocessing objects
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le = joblib.load(le_path)
    
    # Convert input to DataFrame if dict
    if isinstance(new_data, dict):
        new_data = pd.DataFrame([new_data])
    
    # Ensure correct columns and order
    expected_cols = ['AGE', 'PackHistory', 'MWT1Best', 'FEV1', 'FEV1PRED', 'FVC', 'FVCPRED', 
                     'CAT', 'HAD', 'SGRQ', 'AGEquartiles', 'gender', 'smoking', 'Diabetes', 
                     'muscular', 'hypertension', 'AtrialFib', 'IHD']
    new_data = new_data[expected_cols]
    
    # Scale the data
    new_data_scaled = scaler.transform(new_data)
    
    # Predict
    pred = model.predict(new_data_scaled)
    severity = le.inverse_transform(pred)[0]
    
    return severity

# Example Usage
sample_patient = {
    'AGE': 70, 'PackHistory': 40, 'MWT1Best': 300, 'FEV1': 1.5, 'FEV1PRED': 60,
    'FVC': 2.5, 'FVCPRED': 80, 'CAT': 20, 'HAD': 10, 'SGRQ': 50, 'AGEquartiles': 3,
    'gender': 1, 'smoking': 2, 'Diabetes': 0, 'muscular': 0, 'hypertension': 1,
    'AtrialFib': 0, 'IHD': 0
}
prediction = predict_copd_severity(sample_patient)
print(f"Predicted COPD Severity: {prediction}")