from flask_app import app, db, bcrypt
from flask import request
import secrets
from flask import render_template,redirect, url_for
from flask_app.models import Client, Project, Employee
from flask_app.forms import RegistrationForm, LoginForm, CreateClientForm, CreateProjectForm, CreateFeatureForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
@login_required
def home():
	return render_template('home.html')

@app.route('/inst')
@login_required
def inst():
	return render_template('verify_account_instructions.html')

@app.route('/validate',methods=['POST'])
def validate():
	print("chakka");
	if 'email' in request.form and Employee.query.filter_by(email = request.form['email']).first():
		return "error"
	elif 'emp_id' in request.form and Employee.query.filter_by(emp_id = request.form['emp_id']).first():
		return "error"
	else:
		return "OK"


@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		print("inside login")
		employee = Employee.query.filter_by(emp_id=form.emp_id.data).first()
		if employee and bcrypt.check_password_hash(employee.password, form.password.data):
			print("inside bcrypt")
			login_user(employee,remember=false)
			print("inside login user")
			return redirect(url_for('home'))
	return render_template("login.html",form=form)


@app.route("/register",methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		employee = Employee(name=form.name.data,emp_id=form.emp_id.data,email=form.email.data,password=hashed_password)
		db.session.add(employee)
		db.session.commit()
		return render_template('verify_account_instructions.html')
	return render_template('register.html',form=form)



@app.route("/create/client",methods=['GET', 'POST'])
@login_required
def create_client():
	form = CreateClientForm()
	if form.validate_on_submit():
		client = Client(name=form.name.data,email=form.email.data)
		db.session.add(client)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create_client.html',form=form)




@app.route("/create/project",methods=['GET','POST'])
@login_required
def create_project():
	print("chakka")
	form = CreateProjectForm()
	form.client.choices=[( client.id,client.name) for client in Client.query.all()]
	print(form.title.data,form.description.data,form.client.data)
	print(type(form.client.data))
	if form.client.data:
		print("inside thenga")
		try:
			client = Client.query.get(int(form.client.data))
		except ValueError:
			print("Failure w/ value " + form.client.data) 
	print("errors are ",form.errors)
	if form.validate_on_submit():
		print("chakka")
		project = Project(title = form.title.data, description = form.description.data, client_id = int(form.client.data))
		db.session.add(project)
		db.session.commit()
		print(request.content_type)
		return redirect(url_for('home'))
	else:
		print("error is thenga",form.errors)
	return render_template("create_project.html",form=form)




# @app.route("/create/feature")
# def create_feature():
# 	form = CreateFeatureForm()
# 	form.project.choices=[( client.id,client.name) for client in Client.query.all()]
# 	if form.validate_on_submit():
		
