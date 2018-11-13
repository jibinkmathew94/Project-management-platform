from flask_app import app, db
from flask import request
from flask import render_template,redirect, url_for
from flask_app.models import Customer, Project
from flask_app.forms import RegistrationForm, LoginForm, CreateCustomerForm, CreateProjectForm, CreateFeatureForm


@app.route("/")
@app.route("/home")
def home():
	return render_template('layout.html')



@app.route("/create/customer",methods=['GET', 'POST'])
def create_customer():
	form = CreateCustomerForm()
	if form.validate_on_submit():
		customer = Customer(name=form.name.data,email=form.email.data)
		db.session.add(customer)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('register.html',form=form)


@app.route("/create/project",methods=['GET','POST'])
def create_project():
	form = CreateProjectForm()
	form.customer.choices=[(customer.id,customer.name) for customer in Customer.query.all()]
	if form.validate_on_submit():
		print(request.content_type)
		return redirect(url_for('home'))
	return render_template("create_project.html",form=form)


@app.route("/login")
def login():
	return render_template("login.html")


