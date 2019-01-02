from flask_app import app, db, bcrypt
from flask import request, jsonify
from PIL import Image
import secrets
import os
from flask import render_template, redirect, url_for
from flask_app.models import Client, Project, Employee, Feature
from flask_app.forms import (
    RegistrationForm,
    LoginForm,
    CreateClientForm,
    CreateProjectForm,
    CreateFeatureForm,
)
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required
    )


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('home.html')


@login_required
@app.route('/features', methods=['POST'])
def features():
    data = []
    for feature in current_user.features:
        data.append({'title': feature.title,
                    'description': feature.description,
                     'target_date': feature.target_date,
                     'project': feature.project.title,
                     'thumbnails': [{'thumbnail_url': url_for('static', filename='images/' + employee.profile_picture), 'name': employee.name, 'emp_id': employee.emp_id} for employee in feature.employees]})
    return jsonify(data)


@app.route('/inst')
@login_required
def inst():
    return render_template('verify_account_instructions.html')


@app.route('/validate', methods=['POST'])
def validate():
    print("chakka")
    if 'email' in request.form and Employee.query.filter_by(email=request.form['email']).first():
        return "error"
    elif 'emp_id' in request.form and Employee.query.filter_by(emp_id=request.form['emp_id']).first():
        return "error"
    else:
        return "OK"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        print("inside login")
        employee = Employee.query.filter_by(emp_id=form.emp_id.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            print("inside bcrypt")
            login_user(employee, remember=False)
            print("inside login user")
            return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        employee = Employee(name=form.name.data, emp_id=form.emp_id.data, email=form.email.data, password=hashed_password)
        db.session.add(employee)
        db.session.commit()
        return render_template('verify_account_instructions.html')
    return render_template('register.html', form=form)


@app.route("/create/client", methods=['GET', 'POST'])
@login_required
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data, email=form.email.data)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_client.html', form=form)


@app.route("/create/project", methods=['GET', 'POST'])
@login_required
def create_project():
    print("chakka")
    form = CreateProjectForm()
    form.client.choices = [(client.id, client.name) for client in Client.query.all()]
    print(form.title.data, form.description.data, form.client.data)
    print(type(form.client.data))
    if form.client.data:
        print("inside thenga")
        try:
            client = Client.query.get(int(form.client.data))
        except ValueError:
            print("Failure w/ value " + form.client.data)
    print("errors are ", form.errors)
    if form.validate_on_submit():
        print("chakka")
        project = Project(title=form.title.data, description=form.description.data, client_id=int(form.client.data))
        db.session.add(project)
        db.session.commit()
        print(request.content_type)
        return redirect(url_for('home'))
    else:
        print("error is thenga", form.errors)
    return render_template("create_project.html", form=form)


@app.route("/create/feature", methods=['GET', 'POST'])
def create_feature():
    form = CreateFeatureForm()
    form.project.choices = [(project.id, project.title) for project in Project.query.all()]
    form.employees.choices = [(employee.id, employee.name) for employee in Employee.query.all()]
    print(form.target_date.data)
    if form.validate_on_submit():
        feature = Feature(title=form.title.data, description=form.description.data, target_date=form.target_date.data, project_id=form.project.data)
        db.session.add(feature)
        if form.employees.data:
            for employee_id in form.employees.data:
                feature.employees.append(Employee.query.get(employee_id))
            db.session.commit()
            return redirect(url_for('home'))
    else:
        print(form.title.data, form.description.data, form.target_date.data, form.project.data)
    return render_template("create_feature.html", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fp = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fp)
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fp


@login_required
@app.route('/update-image', methods=['POST'])
def update_image():
    print(request.files)
    if 'picture' in request.files:
        picture_path = save_picture(request.files['picture'])
        current_user.profile_picture = picture_path
        db.session.commit()
        return url_for('static', filename='images/' + current_user.profile_picture)
    else:
        return "error", 400


@login_required
@app.route('/account')
def account():
    return render_template('account.html')

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# if form.employees:
            # for employee_id in form.employees.data:
            #     db.session.execute(feature_assign.insert.values(employee_id=employee_id, feature_id=feature.id))