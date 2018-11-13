from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class LoginForm(FlaskForm):
	emp_id = StringField('Emp_id',validators=[DataRequired(), Length(min=5, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class CreateCustomerForm(FlaskForm):
	name = StringField('name',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired(), Email()])
	submit = SubmitField('Add new Customer')

class CreateProjectForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	description = TextAreaField('Content', validators=[DataRequired()])
	customer = SelectField('Client Company',choices=[])
	submit = SubmitField('Create new project')

class CreateFeatureForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	description = TextAreaField('Content', validators=[DataRequired()])
	project = SelectField('Project', coerce=int,choices=[])
	target_date = DateField('Feature completion date',format='%YY-%mm-%dd')
	submit = SubmitField('Create new project')