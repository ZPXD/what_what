from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager
from flask_login import login_required, current_user, login_user, logout_user

import os
import random
from datetime import datetime


here = os.getcwd()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/db/xd.db'.format(here)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = ':)'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


# Main

@app.route('/', methods=["GET", "POST"])
def index():
	'''
	Questions list and main page.
	'''

	# Questions.
	questions = Question.query.all()[:10]

	# Search.
	form = SearchQuestionForm()
	if form.validate_on_submit():
		search = form.search.data
		author = form.search.data
		questions = Question.query.filter(
			Question.question.contains(search),
			Question.author.contains(author)
		)[:10]
	
	# Sort questions by date (newest to oldest).
	questions.sort(key=lambda q : q.date, reverse=True)

	return render_template("index.html", form=form, questions=questions)

@app.route('/question', methods=["GET", "POST"])
def ask_question(): 
	'''
	Question form.
	'''

	if current_user.is_authenticated:
		author = current_user.name
	else:
		author = 'whoops'

	form = QuestionForm()
	if form.validate_on_submit():
		date = time_now()
		question = form.question.data
		question = Question(question=question, date=date, author=author)
		db.session.add(question)
		db.session.commit()
		db.session.flush()
		return redirect(url_for("question", question_id=str(question.id)))
	return render_template('ask_question.html', form=form)

@app.route('/<int:question_id>', methods=["GET", "POST"])
def question(question_id): 
	'''
	List of question answers and question menu.
	'''

	# Question.
	question = Question.query.filter_by(id=int(question_id)).first()
	
	# Answer button.
	button = AnswerButton()
	if button.validate_on_submit():
		return redirect(url_for("answer_question", question_id=str(question_id)))

	# Question Answers.
	question_answers = QuestionAnswers.query.filter_by(question_id=int(question_id)).all()
	question_answers.sort(key=lambda q : q.date, reverse=True)

	return render_template('question.html', button=button, question=question, question_answers=question_answers, n_answers=1)

@app.route('/<int:question_id>/<int:n_answers>', methods=["GET", "POST"])
def show_n_answers(question_id, n_answers=1): 
	print(type(n_answers))
	question = Question.query.filter_by(id=question_id).first()
	all_question_answers = QuestionAnswers.query.filter_by(question_id=question_id).all()
	if all_question_answers:
		try:
			question_answers = random.sample(all_question_answers, n_answers)
		except:
			question_answers = random.sample(all_question_answers, 1)
		question_answers.sort(key=lambda q : q.date, reverse=True)

	else:
		return "no answers yet"
	button = ReoladPageButton(n_answers=n_answers)
	if button.validate_on_submit():
		n_answers = int(button.n_answers.data) # recode
		if not n_answers or n_answers > len(all_question_answers) or n_answers < 1:
			n_answers = 1
		return redirect( url_for('show_n_answers', question_id=int(question_id), n_answers=n_answers))
	return render_template('show_n_answers.html', button=button, question=question, question_answers=question_answers, n_answers=int(n_answers))

@app.route('/<int:question_id>/answer', methods=["GET", "POST"])
def answer_question(question_id):
	'''
	Answer question.
	'''
	if current_user.is_authenticated:
		author = current_user.name
	else:
		author = 'whoops'

	form = QuestionAnswerForm()
	if form.validate_on_submit():
		question_id = int(question_id)
		date = time_now()
		answer_1 = form.answer_1.data
		answer_2 = form.answer_2.data
		answer_3 = form.answer_3.data
		answer_4 = form.answer_4.data
		answer_5 = form.answer_5.data
		answers = [answer_1, answer_2, answer_3, answer_4, answer_5]
		for i, answer in enumerate(answers):
			if answer == '':
				continue

			question_answer = QuestionAnswers(author=author, question_id=question_id, answer=answer, answer_n=i, date=date)	
			db.session.add(question_answer)
			db.session.commit()

		what_else = form.what_else.data
		what_else_answers = WhatElseAnswers(author=author, question_id=question_id, what_else=what_else, date=date)
		db.session.add(what_else_answers)
		db.session.commit()

		return redirect(url_for("question", question_id=str(question_id)))
	return render_template('answer_question.html', form=form)

@app.route('/<int:question_id>/<int:n>', methods=["GET", "POST"])
def question_answers_random(question_id, n):
	'''
	Question answers - random N.
	'''
	answers_list = [] # Questions.query.filter_by(x=x).all()
	return render_template('question_answers_random.html', questions_list=questions_list)

@app.route('/<int:question_id>/t/<int:n>', methods=["GET", "POST"])
def question_answers_random_top(question_id, n):
	'''
	Question answers - top random N.
	'''
	answers_list = [] # Questions.query.filter_by(x=x).all()
	return render_template('question_answers_random_top.html', questions_list=questions_list)


@app.route('/<int:question_id>/<owner>', methods=["GET", "POST"])
def question_decks(question_id, owner):
	'''
	Question list.
	'''

	decks_list = [] # Decks.query.filter_by(x=x).all()
	return render_template('question_decks.html', decks_list=decks_list)

@app.route('/<int:question_id>/<owner>/<int:deck_id>', methods=["GET", "POST"])
def question_deck(question_id, owner, deck_id):
	'''
	Question deck.
	'''
	questions = [] # Questions.query.filter_by(x=x).all()
	return render_template('question_deck.html', questions=questions)

# Helpers

def time_now():
	return datetime.now()


# Login

@login_manager.user_loader
def load_user(user_id):
	user = User.query.get(user_id)
	return user

@app.route('/login', methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()
		user.last_login = time_now()
		db.session.add(user)
		db.session.commit()

		if user:
			if user.check_password(password):
				login_user(user, force=True)
				return redirect( url_for('index'))
		else:
			return "user not found"

	return render_template("login.html", form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
	form = SignupForm()
	if form.validate_on_submit():

		join_date = time_now()
		last_login = time_now()
		name = form.name.data
		email = form.email.data
		password = form.password.data
		confirm_password = form.confirm_password.data

		if User.query.filter_by(email=email).first():
			return 'taki email już istnieje'

		user = User(name=name, email=email, password=password, join_date=join_date, last_login=last_login)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()

		return redirect( url_for('index'))
	return render_template("signup.html", form=form)

@login_required
@app.route('/logout')
def logout():
	logout_user()
	return render_template("logout.html")


@login_required
@app.route('/profile/<name>', methods=["GET", "POST"])
def user_profile(name):
	'''
	User profile.
	'''
	if name != current_user.name:
		return "no"

	# User questions.
	questions = Question.query.filter(Question.author.contains(name))[:10]

	# User questions search.
	form = SearchQuestionForm()
	if form.validate_on_submit():
		search = form.search.data
		questions = Question.query.filter(
			Question.question.contains(search),
			Question.author.contains(name)
		)[:10]

	# Sort questions by date (newest to oldest).
	questions.sort(key=lambda q : q.date, reverse=True)

	return render_template("profile.html", form=form, questions=questions)


# DB Models

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	join_date = db.Column(db.DateTime)
	last_login = db.Column(db.DateTime)
	name = db.Column(db.String(120), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))

	def set_password(self,password):
		self.password = generate_password_hash(password)
	 
	def check_password(self, password):
		return check_password_hash(self.password, password)

	def __repr__(self):
		return '<User {}>'.format(self.name)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	author = db.Column(db.String(303))
	question = db.Column(db.String(303))

class QuestionAnswers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	question_id = db.Column(db.Integer)
	author = db.Column(db.String(120)) 
	answer = db.Column(db.String(120))
	answer_n = db.Column(db.Integer)

class WhatElseAnswers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	question_id = db.Column(db.Integer)
	author = db.Column(db.String(120))
	what_else = db.Column(db.String(120))
	


# Forms

class AnswerButton(FlaskForm):
	button = SubmitField('Answer')

class ReoladPageButton(FlaskForm):
	n_answers = StringField(default=1)
	button = SubmitField('Next answer')

class SearchQuestionForm(FlaskForm):
	search = StringField()
	author = StringField()
	button = SubmitField('Search')

class QuestionForm(FlaskForm):
	question = StringField(validators=[DataRequired()])
	button = SubmitField('Ask')

class QuestionAnswerForm(FlaskForm):
	answer_1 = StringField(validators=[DataRequired()])
	answer_2 = StringField()
	answer_3 = StringField()
	answer_4 = StringField()
	answer_5 = StringField()
	what_else = StringField()
	button = SubmitField('Answer')

class LoginForm(FlaskForm):
	email = StringField(validators=[DataRequired()])
	password = StringField(validators=[DataRequired()])
	button = SubmitField('login')

class SignupForm(FlaskForm):
	name = StringField(validators=[DataRequired()])
	email = StringField(validators=[DataRequired()])
	password = StringField(validators=[DataRequired()])
	confirm_password = StringField(validators=[DataRequired()])
	button = SubmitField('sign up')


@app.before_first_request
def create_all():
	if not 'db' in os.listdir():
		os.mkdir('db')	
	db.create_all()


# Errors

@app.errorhandler(404)
def handle_404(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
	return render_template('500.html'), 500


if __name__=="__main__":
	app.run(debug=True)