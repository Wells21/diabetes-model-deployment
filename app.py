from flask import Flask, render_template, request
import joblib
import pandas as pd


loaded_scaler = joblib.load('models/scaler.joblib')
loaded_model = joblib.load('models/trained_model2.joblib')

app = Flask(__name__)

# defining a function that collects users input, convert to a dataframe, preprocesses the data, and make predictions with a degree of certainty

def prediction(gender, age, hypertension, heart_disease, bmi, HbA1c_level, blood_glucose_level):

    dic = {
        'gender': [gender],
        'age': [age],
        'hypertension': [hypertension], 
        'heart_disease': [heart_disease], 
        'bmi': [bmi],
        'HbA1c_level': [HbA1c_level],
        'blood_glucose_level': [blood_glucose_level]
    }
    
    user_input = pd.DataFrame(dic)
    
    numeric_cols = ['gender', 'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    
    # mapping the gender column to Male : 1, Female : 0
    user_input['gender'] = user_input['gender'].map({'Male': 1, 'Female': 0})
    user_input['hypertension'] = user_input['hypertension'].map({'Yes': 1, 'No': 0})
    user_input['heart_disease'] = user_input['heart_disease'].map({'Yes': 1, 'No': 0})
    
    user_input[numeric_cols] = loaded_scaler.transform(user_input[numeric_cols])
    
    pred = loaded_model.predict(user_input)
    pred_proba = loaded_model.predict_proba(user_input)
    
    if pred == 1:
        return "Patient has a {:.2f}% likelihood of been diagnosed with Diabetes.".format(pred_proba[:, 1][0] * 100)
    
    else:
        return "Patient does not have Diabetes with a given probabilty of {:.2f}%".format(pred_proba[:, 0][0] * 100)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    gender = request.form.get('gender')
    age = request.form.get('age')
    hypertension = request.form.get('hypertension')
    heart_disease = request.form.get('heartDisease')
    bmi = request.form.get('bmi')
    hemoglobin = request.form.get('hemoglobinA1c')
    bloodglucose = request.form.get('bloodGlucose')

    age = int(age)
    bmi = float(bmi)
    hemoglobin = float(hemoglobin)
    bloodglucose = float(bloodglucose)

    result = prediction(gender, age, hypertension, heart_disease, bmi, HbA1c_level = hemoglobin, blood_glucose_level = bloodglucose)

    return render_template("index.html", text=result, gender=gender, age=age, hypertension=hypertension, heart_disease=heart_disease, bmi=bmi, hemoglobin=hemoglobin, bloodglucose=bloodglucose)

if __name__ == "__main__":
    app.run(debug=True)