from flask import Flask
from flask import request
import json

app = Flask(__name__)
get_msg = ""
patients_poz = []  # patients from Poznan
patients_wro = []  # patients from Wroclaw
patients_war = []  # patients from Warsaw


@app.route('/')
def hello():
    return "Welcome to patients database.\n" \
           "You can choose one of the following cities:\n" \
           "Poznan, Wroclaw, Warsaw\n" \
           "You can manage patients database," \
           " or print list of patients located in certain city."


@app.route('/<user>', methods=['GET'])
def hello_user(user):
    return "Hello {}!".format(user) + " You sucessfully logged in."


@app.route('/<user>/<city>/patients', methods=['GET'])
def return_patients(user, city):
    global patients_poz
    global patients_war
    global patients_wro
    print("User: " + format(user) + " request on city: " + format(city))
    if format(city) == 'poznan':
        return json.dumps(patients_poz)
    elif format(city) == 'warsaw':
        return json.dumps(patients_war)
    elif format(city) == 'wroclaw':
        return json.dumps(patients_wro)
    else:
        return "Invaid city."


@app.route('/<user>/<city>/<patient_id>', methods=['GET'])
def hello_name(user, city, patient_id):
    global patients_poz
    global patients_war
    global patients_wro
    print("User: " + format(user) + ", request on city: " + format(city) +
          ", patient ID: " + format(patient_id))
    if format(city) == 'poznan':
        for patient in patients_poz:
            if patient['patient_id'] == format(patient_id):
                return json.dumps(patient)
        return json.dumps(patients_poz)
    elif format(city) == 'warsaw':
        for patient in patients_war:
            if patient['patient_id'] == format(patient_id):
                return json.dumps(patient)
    elif format(city) == 'wroclaw':
        for patient in patients_wro:
            if patient['patient_id'] == format(patient_id):
                return json.dumps(patient)
    else:
        return "Invaid argment."


@app.route('/<user>/<city>/add', methods=['POST'])
def add_patient(user, city):
    global patients_poz
    global patients_war
    global patients_wro
    json_obj = json.loads(request.data)
    print("User: " + format(user) + " request on city: " + format(city) +
          " added patient with ID: " + json_obj['patient_id'])
    if format(city) == 'poznan':
        patients_poz.append(json_obj)
    elif format(city) == 'warsaw':
        patients_war.append(json_obj)
    elif format(city) == 'wroclaw':
        patients_wro.append(json_obj)
    else:
        return "Invaid argument."
    return "Patient with ID: " + json_obj['patient_id'] + " was succsessfully" \
                                                          "added to database."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
