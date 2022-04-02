from flask import Flask, render_template
from flask_wtf import FlaskForm


from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
	StringField,
	TextAreaField,
	SubmitField,
	PasswordField,
	DateField,
	SelectField
)

app=Flask(__name__)

app.secret_key = 'super secret key'

@app.route('/', methods=["GET", "POST"])
def index():
	return render_template("index.html")


# Logowanie

@app.route('/login', methods=["GET", "POST"])
def login():
	return 'login'

@app.route('/signup', methods=["GET", "POST"])
def signup():
	form = SignupForm()

	if form.validate_on_submit():
		user = form.user.data
		password = form.password.data
		email = form.email.data
	
	return render_template("signup.html", form=form)

@app.route('/logout', methods=["GET", "POST"])
def logout():
	return 'logout'


@app.route('/signup_success', methods=["GET", "POST"])
def signup_success():
	return render_template("signup_success.html")






@app.route('/ask_question', methods=["GET", "POST"])
def question():
	return "question"

@app.route('/answer', methods=["GET", "POST"])
def answer():
	return "answer"

@app.route('/', methods=["GET", "POST"])
def list_of_questions():
	return "list of questions"

@app.route('/', methods=["GET", "POST"])
def show_random_answer():
	return "random answer"

@app.route('/', methods=["GET", "POST"])
def show_list_of_answers():
	return "list of answers"



class SignupForm(FlaskForm):
	user = StringField('Login')
	password = PasswordField('Password')
	confirm_password = PasswordField('Repeat Password')
	email = StringField('Email')
	#recaptcha = RecaptchaField()
	submit = SubmitField('Submit')

	#password = PasswordField('New Password', [
	#        validators.DataRequired(),
	#        validators.EqualTo('confirm', message='Passwords must match')
	#])


if __name__=="__main__":
	app.run(host='0.0.0.0')
