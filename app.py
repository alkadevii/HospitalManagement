from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from datetime import date

# 🔐 Load environment variables
load_dotenv()

app = Flask(__name__)

# 🔗 MongoDB Connection (from .env)
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
patients = db["patients"]
doctors = db["doctors"]
appointments = db["appointments"]

# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')


# -------------------- PATIENT --------------------

@app.route('/add_patient', methods=['GET', 'POST'])
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


@app.route('/patients')
def view_patients():
    return render_template('patients.html', patients=list(patients.find()))


# -------------------- DOCTOR --------------------

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        doctors.insert_one({
            "name": request.form['name'],
            "specialization": request.form['specialization'],
            "phone": request.form['phone']
        })
        return redirect('/')
    return render_template('add_doctor.html')


# -------------------- APPOINTMENT --------------------

@app.route('/add_appointment', methods=['GET', 'POST'])
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

    return render_template(
        'add_appointment.html',
        patients=list(patients.find()),
        doctors=list(doctors.find())
    )


# -------------------- PATIENT HISTORY --------------------

@app.route('/patient_history/<pid>')
def patient_history(pid):
    patient = patients.find_one({"_id": ObjectId(pid)})
    patient_appointments = list(appointments.find({"patient_id": ObjectId(pid)}))

    for appt in patient_appointments:
        doctor = doctors.find_one({"_id": appt["doctor_id"]})
        appt["doctor_name"] = doctor["name"] if doctor else "N/A"
        appt["specialization"] = doctor["specialization"] if doctor else "N/A"

    return render_template(
        'patient_history.html',
        patient=patient,
        appointments=patient_appointments
    )


# -------------------- DOCTOR APPOINTMENTS --------------------

@app.route('/doctor_appointments')
def doctor_appointments():
    did = request.args.get('did')
    today = str(date.today())

    doctor = doctors.find_one({"_id": ObjectId(did)})

    today_appts = list(appointments.find({
        "doctor_id": ObjectId(did),
        "date": today
    }))

    for appt in today_appts:
        patient = patients.find_one({"_id": appt["patient_id"]})
        appt["patient_name"] = patient["name"] if patient else "N/A"
        appt["phone"] = patient["phone"] if patient else "N/A"

    return render_template(
        "doctor_appointments.html",
        doctor=doctor,
        appointments=today_appts
    )


# -------------------- RUN --------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)