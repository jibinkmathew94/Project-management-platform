from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
    DateField,
    SelectMultipleField
)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import (
    DataRequired,
    Length, 
    Email,
    EqualTo,
    ValidationError
)
from wtforms.widgets import (
    TextInput,
    PasswordInput,
)


class TextDataBindWidget(TextInput):
    def __call__(self, field, **kwargs):
        for key in kwargs:
            if key == 'data_bind':
                kwargs['data-bind'] = kwargs.pop(key)
        return super().__call__(field, **kwargs)


class PasswordDataBindWidget(PasswordInput):
    def __call__(self, field, **kwargs):
        for key in kwargs:
            if key == 'data_bind':
                kwargs['data-bind'] = kwargs.pop(key)
        return super().__call__(field, **kwargs)


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    emp_id = StringField('Emp id', validators=[DataRequired(), Length(min=5, max=5, message="Emp id should be 5 characters")], widget=TextDataBindWidget())
    email = StringField('Email', validators=[DataRequired(), Email()], widget=TextDataBindWidget())
    password = PasswordField('Password', validators=[DataRequired()], widget=PasswordDataBindWidget())
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Entered passwords do not match')], widget=PasswordDataBindWidget())
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    emp_id = StringField('Emp id', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateClientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add new Client')


class CreateProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    client = SelectField('Client Company', coerce=int, choices=[])
    submit = SubmitField('Create new project')


class CreateFeatureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Content', validators=[DataRequired()])
    project = SelectField('Project', coerce=int, choices=[])
    employees = SelectMultipleField('Members', coerce=int, choices=[])
    target_date = DateField('Feature completion date', format='%Y-%m-%d')
    submit = SubmitField('Create new project')
