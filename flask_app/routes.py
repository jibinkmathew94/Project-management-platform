from flask_app import app
from flask import render_template

@app.route("/")
@app.route("/home")
def home():
	return render_template('base_layout.html')


@app.route("/about")
def about():
	return("about")