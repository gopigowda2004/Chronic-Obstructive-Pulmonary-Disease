---
# 🫁 COPD Prediction Web App

The **COPD Prediction Web App** is a lightweight and user-friendly platform that predicts the likelihood of Chronic Obstructive Pulmonary Disease (COPD) based on health-related data provided by users. The application features a responsive frontend built with HTML, CSS, and JavaScript, a Python Flask backend, and uses a JSON file as a NoSQL database to store user inputs and predictions.

## 🚀 Features

- Interactive and responsive UI for easy data input  
- Real-time COPD risk prediction using a trained ML model  
- Backend built with Flask for handling logic and requests  
- Stores data persistently in a NoSQL JSON format  
- Lightweight, fast, and easy to deploy

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python Flask  
- **Machine Learning:** Scikit-learn, Pickle (.pkl model)  
- **Database:** JSON File (NoSQL structure)

## 📁 Project Structure
```
copd-prediction-app/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   └── index.html
├── data/
│   └── users.json
├── model/
│   └── copd_model.pkl
├── app.py
├── requirements.txt
└── README.md
```
## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/copd-prediction-app.git
cd copd-prediction-app
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask App
```bash
python app.py
```

The application will be accessible at: `http://127.0.0.1:5000`

## 🧠 How It Works

1. User inputs health data through a web form.
2. The frontend sends the data to the Flask backend.
3. The backend loads a trained ML model (`copd_model.pkl`) to predict COPD risk.
4. The result is displayed to the user and stored in a local JSON file for record keeping.

## 📄 Sample JSON Data Entry

```json
[
  {
    "name": "Alice Smith",
    "age": 60,
    "smoking_history": "Yes",
    "lung_capacity": 70,
    "prediction": "High Risk",
    "timestamp": "2025-04-14T11:00:00"
  }
]
```

## 🔮 Future Enhancements

- User authentication and login system  
- Graphical dashboard with data visualizations  
- Integration with MongoDB or Firebase  
- API endpoints for mobile or third-party apps  
- Deployment on cloud platforms like Heroku, Render, or AWS

## 👨‍💻 Author

**Muhammed Biilal S**  
Founder & Developer  
GitHub: [https://github.com/2003MBS](https://github.com/2003MBS) 
LinkedIn: [www.linkedin.com/in/muhammed-bilal-s-61376a229](www.linkedin.com/in/muhammed-bilal-s-61376a229)

## 📃 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute for personal or commercial purposes.

---

Let me know if you'd like a downloadable version or if you're planning to deploy it somewhere—I can help you set that up too!

