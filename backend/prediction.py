import pandas as pd
import joblib

def predict_copd_severity(new_data, model_path='backend/copd_rf_model.pkl', scaler_path='backend/scaler.pkl', le_path='backend/label_encoder.pkl'):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le = joblib.load(le_path)
    if isinstance(new_data, dict):
        new_data = pd.DataFrame([new_data])
    expected_cols = ['AGE', 'PackHistory', 'MWT1Best', 'FEV1', 'FEV1PRED', 'FVC', 'FVCPRED', 
                     'CAT', 'HAD', 'SGRQ', 'AGEquartiles', 'gender', 'smoking', 'Diabetes', 
                     'muscular', 'hypertension', 'AtrialFib', 'IHD']
    new_data = new_data[expected_cols]
    new_data_scaled = scaler.transform(new_data)
    # Get probabilities
    probs = model.predict_proba(new_data_scaled)[0]
    pred = model.predict(new_data_scaled)
    severity = le.inverse_transform(pred)[0]
    # Print probabilities for each class
    prob_dict = {le.classes_[i]: round(prob, 3) for i, prob in enumerate(probs)}
    return severity, prob_dict

if __name__ == "__main__":
    sample_patient = {
        'AGE': 70, 'PackHistory': 40, 'MWT1Best': 500, 'FEV1': 3.5, 'FEV1PRED': 90,
        'FVC': 2.5, 'FVCPRED': 80, 'CAT': 5, 'HAD': 10, 'SGRQ': 50, 'AGEquartiles': 3,
        'gender': 1, 'smoking': 2, 'Diabetes': 0, 'muscular': 0, 'hypertension': 1,
        'AtrialFib': 0, 'IHD': 0
    }
    severity1, probs1 = predict_copd_severity(sample_patient)
    print(f"Predicted COPD Severity: {severity1}")
    print(f"Probabilities: {probs1}")
    
    another_patient = {
        'AGE': 65, 'PackHistory': 20, 'MWT1Best': 400, 'FEV1': 2.0, 'FEV1PRED': 80,
        'FVC': 3.0, 'FVCPRED': 90, 'CAT': 15, 'HAD': 5, 'SGRQ': 30, 'AGEquartiles': 2,
        'gender': 0, 'smoking': 1, 'Diabetes': 1, 'muscular': 0, 'hypertension': 0,
        'AtrialFib': 0, 'IHD': 1
    }
    severity2, probs2 = predict_copd_severity(another_patient)
    print(f"Predicted COPD Severity for second patient: {severity2}")
    print(f"Probabilities: {probs2}")