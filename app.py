from flask import Flask, render_template

app=Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    return "<h1> style=center>what what</h1>" #render_template("index.html")

# Widok dla zalogowanego użytkownika. ['logout']
# Widok dla wylogowanego użytkownika. ['login' / 'signup']

@app.route('/login', methods=["GET", "POST"])
def login():
	return 'login'

@app.route('/signup', methods=["GET", "POST"])
def signup():
	return 'login'

@app.route('/logout', methods=["GET", "POST"])
def logout():
	return 'login'

@app.route('/ask_question', methods=["GET", "POST"])
def question():
	return "question"

@app.route('/answer', methods=["GET", "POST"])
def answer():
	return "answer"

@app.route('/list_of_questions', methods=["GET", "POST"])
def list_of_questions():
	return "list of questions"

@app.route('/random_answer', methods=["GET", "POST"])
def show_random_answer():
	return "random answer"

@app.route('/list_of_answers', methods=["GET", "POST"])
def show_list_of_answers():
	return "list of answers"


if __name__=="__main__":
    app.run(host='0.0.0.0')
