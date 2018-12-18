from flask_login import UserMixin
from flask_app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

features = db.Table('features',
	db.Column('employee_id',db.Integer,db.ForeignKey('employee.id'),primary_key=True),
	db.Column('feature_id',db.Integer,db.ForeignKey('feature.id'),primary_key=True),
)

class Employee(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	emp_id = db.Column(db.String(30), unique=True, nullable=False)
	name = db.Column(db.String(30), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	features = db.relationship('Feature', secondary=features, lazy=True,
		backref=db.backref('employees', lazy='joined'))
	admin	= db.Column(db.Boolean,unique=False,default=False)
	verified = db.Column(db.Boolean,unique=False,default=False)

	def __repr__(self):
		return f'Employee {self.name}, Emp_id : {self.emp_id} email : {self.email}'



class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	def __repr__(self):
		return f'Client {self.name},email : {self.email}'



class Project(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(30), unique=True, nullable=False)
	description = db.Column(db.Text, nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	client = db.relationship("Client",backref="Projects")

	def __repr__(self):
		return f'Project {self.title}'



class Feature(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(30), nullable=False)
	description = db.Column(db.Text, nullable=False)
	target_date = db.Column(db.DateTime, nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
	project = db.relationship("Project",backref="features")
	def __repr__(self):
		return f'Feature {self.title},email : {self.project}'




# class Description(db.Model):
# 	id = db.Column(db.Integer,primary_key=True)
# 	priority = db.Column(db.Integer,nullable=False)
# 	description = db.Column(db.Text, nullable=False)