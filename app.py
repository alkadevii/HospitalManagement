from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 🔗 MongoDB Atlas Connection
client = MongoClient("mongodb+srv://alkadevi012_db_user:OnRTmUp5LekB5yJ9@hospital.jjujfob.mongodb.net/")
db = client["hospital_db"]

patients = db["patients"]
doctors = db["doctors"]
appointments = db["appointments"]

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Add Patient
@app.route('/add_patient', methods=['GET','POST'])
def add_patient():
    if request.method == 'POST':
        patients.insert_one({
            "name": request.form['name'],
            "age": int(request.form['age']),
            "gender": request.form['gender'],
            "phone": request.form['phone'],
            "address": request.form['address']
        })
        return redirect('/')
    return render_template('add_patient.html')

# View Patients
@app.route('/patients')
def view_patients():
    data = list(patients.find())
    return render_template('patients.html', patients=data)

# Add Doctor
@app.route('/add_doctor', methods=['GET','POST'])
def add_doctor():
    if request.method == 'POST':
        doctors.insert_one({
            "name": request.form['name'],
            "specialization": request.form['specialization'],
            "phone": request.form['phone']
        })
        return redirect('/')
    return render_template('add_doctor.html')

# Add Appointment
@app.route('/add_appointment', methods=['GET','POST'])
def add_appointment():
    if request.method == 'POST':
        appointments.insert_one({
            "patient_id": ObjectId(request.form['pid']),
            "doctor_id": ObjectId(request.form['did']),
            "date": request.form['date'],
            "time": request.form['time'],
            "status": "Scheduled"
        })
        return redirect('/')
    return render_template('add_appointment.html')

if __name__ == '__main__':
    app.run(debug=True)