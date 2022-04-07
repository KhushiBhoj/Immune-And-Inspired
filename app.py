from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pbl3'

db = SQLAlchemy(app)
class Contactus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)

model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():

    return render_template('home.html')

@app.route("/read")
def info():
    
    return render_template('read.html')

@app.route("/result")
def result():
    
    return render_template('result.html')

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == 'GET':
        text = "Result: "
    elif request.method == 'POST':
        test = request.form.get('test_method')
        h, mch, mchc, mcv = 0, 0, 0, 0
        if test == "Hemoglobin":
            min = 11.5
            max = 16.5
            h = 1
        elif test == "MCH":
            min = 27
            max = 32
            mch = 1
        elif test == "MCHC":
            min = 30
            max = 35
            mchc = 1
        else:
            min = 76
            max = 96
            mcv = 1
        result = request.form.get('Result')
        # print(result, min, max, h, mch, mchc, mcv)
        final_values = np.array([result, min, max, h, mch, mchc, mcv]).reshape(1, -1)
        prediction = model.predict(final_values)
        print(prediction)
        if prediction[0] == 0:
            text = "Result: Our Model Predicts that you are Anaemia Negative." 
        else:
            text = "Result: Our Model Predicts that you are Anaemia Positive."
    return render_template('predict.html', predicted_text = text)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')
        entry = Contactus(name=name, email = email, feedback = feedback)
        db.session.add(entry)
        db.session.commit()
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)