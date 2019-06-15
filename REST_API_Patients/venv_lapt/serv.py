from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import json
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pamperek'
patients = []
employees = []


class Employee:
    id

    def __init__(self, public_id, name, surname, password, admin):
        self.public_id = public_id  # for protection purposes
        self.name = name
        self.surname = surname
        self.password = password
        self.admin = admin


class Patient:
    def __init__(self, id, name, surname, age, ward, diagnosis, sign_out, last_modified_by):
        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.ward = ward
        self.diagnosis = diagnosis
        self.sign_out = sign_out
        self.last_modified_by = last_modified_by


def initialize_admin():
    hashed_password = generate_password_hash('admin', method='sha256')
    new_employee = Employee(public_id=str(uuid.uuid4()), name='Admin',
                            surname='Admin', password=hashed_password, admin=True)
    employees.append(new_employee)


# creating a decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # if token is in a header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:  # if there is no token passed
            return jsonify({'message': 'No token found.'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])  # token data
            for employee in employees:
                if employee.public_id == data['public_id']:
                    current_employee = employee
        except:
            return jsonify({'message': 'Invalid token.'}, 401)

        return f(current_employee, *args, **kwargs)

    return decorated


@app.route('/employees', methods=['GET'])
@token_required
def get_all_employees(current_employee):
    if not current_employee.admin:
        return jsonify({'message': 'Only admin can perform that task.'})

    output = []
    for employee in employees:
        output.append(json.dumps(employee.__dict__))
    return jsonify({'employees': output})


@app.route('/employee/<public_id>', methods=['GET'])
@token_required
def get_one_employee(current_employee, public_id):
    if not current_employee.admin:
        return jsonify({'message': 'Only admin can perform that task.'})

    for employee in employees:
        if employee.public_id == public_id:
            return json.dumps(employee.__dict__)
    if not employee.public_id == public_id:
        return jsonify({'message': 'No employee found.'})


@app.route('/employee', methods=['POST'])
@token_required
def add_employee(current_employee):
    if not current_employee.admin:
        return jsonify({'message': 'Only admin can perform that task.'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_employee = Employee(public_id=str(uuid.uuid4()), name=data['name'],
                            surname=data['surname'], password=hashed_password, admin=False)
    employees.append(new_employee)
    return jsonify({'message': 'New employee added.'})


@app.route('/employee/<public_id>', methods=['PUT'])
@token_required
def promote_employee(current_employee, public_id):  # makes an employee an admin
    if not current_employee.admin:
        return jsonify({'message': 'Only admin can perform that task.'})

    for employee in employees:
        if employee.public_id == public_id:
            employee.admin = True
            return jsonify({'message': 'Employee is know an admin.'})  # json.dumps(employee.__dict__)
    if not employee.public_id == public_id:
        return jsonify({'message': 'No employee found.'})


@app.route('/employee/<public_id>', methods=['DELETE'])
@token_required
def delete_employee(current_employee, public_id):
    if not current_employee.admin:
        return jsonify({'message': 'Only admin can perform that task.'})

    for employee in employees:
        if employee.public_id == public_id:
            employees.remove(employee)
            return jsonify({'message': 'Employee has been deleted.'})
    if not employee.public_id == public_id:
        return jsonify({'message': 'No employee found.'})


@app.route('/login')  # only this endpoint works with authentication, other work with token
def login():
    auth = request.authorization

    # when user doesn't supply any authorization data
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401,
                             {'WWW-Authenticate': 'Basic realm="Login required."'})

    # when everything is correct
    for employee in employees:
        if employee.surname == auth.username:
            if check_password_hash(employee.password, auth.password):
                token = jwt.encode({'public_id': employee.public_id, 'exp': datetime.datetime.utcnow()
                                                                            + datetime.timedelta(minutes=60)},
                                   app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})  # returns token vaild for 1 h

    # when there is no user on the list
    if not employee.surname == auth.username:
        return make_response('Could not verify', 401,
                             {'WWW-Authenticate': 'Basic realm="Login required."'})

    # when password is incorrect
    return make_response('Could not verify', 401,
                         {'WWW-Authenticate': 'Basic realm="Login required."'})


@app.route('/patients', methods=['GET'])
@token_required
def get_all_patients(current_employee):
    output = []
    for patient in patients:
        output.append(json.dumps(patient.__dict__))
    return jsonify({'patients': output})


@app.route('/patient/<patient_id>', methods=['GET'])
@token_required
def get_one_patient(current_employee, patient_id):
    for patient in patients:
        if patient.id == patient_id:
            return json.dumps(patient.__dict__)
    if not patient.id == patient_id:
        return jsonify({'message': 'No patient found.'})


@app.route('/patient', methods=['POST'])
@token_required
def add_patient(current_employee):
    data = request.get_json()

    new_patient = Patient(id=str(uuid.uuid4()), name=data['name'], surname=data['surname'],
                          age=data['age'], ward=data['ward'], diagnosis=data['diagnosis'], sign_out=False,
                          last_modified_by=current_employee.public_id)
    patients.append(new_patient)
    print(current_employee.public_id)
    return jsonify({'message': 'New patient added.'})


@app.route('/patient/<patient_id>', methods=['PUT'])
@token_required
def sign_out_patient(current_employee, patient_id):
    for patient in patients:
        if patient.id == patient_id:
            patient.sign_out = True
            patient.last_modified_by = current_employee.public_id
            return jsonify({'message': 'Patient is signed out.'})
    if not employee.public_id == public_id:
        return jsonify({'message': 'No patient found.'})


@app.route('/patient/<patient_id>', methods=['DELETE'])
@token_required
def delete_patient(current_employee, patient_id):
    for patient in patients:
        if patient.id == patient_id:
            patients.remove(patient)
            return jsonify({'message': 'Patient has been deleted.'})
    if not patient.id == patient_id:
        return jsonify({'message': 'No patient found.'})


if __name__ == '__main__':
    initialize_admin()
    app.run(host='0.0.0.0', port=80)
