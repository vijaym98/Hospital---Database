from flask import Flask, render_template, request, session, make_response
from data import Database
from models.hospital import Hospital
from models.patient import Patient
from models.user import User

app = Flask(__name__)
app.secret_key = "vijay"



@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
    if session['email'] == None: return "Something wrong, try again"

    return render_template("profile.html")


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])


@app.route('/hospitals/<string:user_id>')
@app.route('/hospitals')
def hospitals1(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    hospitals = user.get_hospitals()

    return render_template("hospitals.html", hospitals=hospitals, email=user.email)


@app.route('/hospitals/new', methods=['POST', 'GET'])
def new_hospital():
    if request.method == 'GET':
        return render_template('new_hospital.html')
    else:
        name = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_hospital = Hospital(user.email, name, description, user._id)
        new_hospital.save_to_mongo()

        return make_response(hospitals1(user._id))


@app.route('/patients/<string:hospital_id>')
def hospital_patients(hospital_id):
    hospital = Hospital.from_mongo(hospital_id)
    patients = hospital.get_patients()

    return render_template('patients.html', patients=patients, hospital_title=hospital.name, hospital_id=hospital._id)


@app.route('/patients/new/<string:hospital_id>', methods=['POST', 'GET'])
def new_patient(hospital_id):
    if request.method == 'GET':
        return render_template('new_patient.html', hospital_id=hospital_id)
    else:
        name = request.form['title']
        details = request.form['content']
        user = User.get_by_email(session['email'])

        new_patient = Patient(hospital_id, name, details, user.email)
        new_patient.save_to_mongo()

        return make_response(hospital_patients(hospital_id))


if __name__ == '__main__':
    app.run(port=4994, debug=True)