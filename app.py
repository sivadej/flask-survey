from flask import Flask, render_template, request, url_for, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_modus3 import Modus
from surveys import Survey, Question, satisfaction_survey

app = Flask(__name__)
modus = Modus(app)

# enable toolbar in debug mode only. In production, set to False to disable toolbar.
app.debug = False

# set a secret key to enable Flask session cookies
app.config['SECRET_KEY'] = 'yo'

# prevent debugtoolbar from interrupting redirects
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

# survey responses should be stored into this list.
# example of response:
#     ['Yes', 'No', 'Less than $10,000', 'Yes']
responses = []
survey = satisfaction_survey


@app.route('/')
def index():
    return render_template('survey_index.html', title=survey.title, instructions=survey.instructions)


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
def questions(id):
    # protect questions - keep track of progress and dont allow user to manually enter ID as url,
    #   return them to current question

    if request.method == 'POST':
        user_response = request.form['response']
        print(f'user_response received for question {id}: {user_response}')
        responses.append(user_response)
        next_id = id+1
        for response in responses:
            print(response)
        # redirect to thank you page once final question is answered
        if next_id >= len(survey.questions):
            return redirect(url_for('results'))
        else:
            return redirect(url_for('questions', id=next_id))
    return render_template('survey_question.html', title=survey.title, question=survey.questions[id])


@app.route('/results')
def results():
    return render_template('survey_results.html', title=survey.title, results=responses)


@app.route('/thanks')
def thanks():
    return "thank you!"


# 2/25 TO-DO refactor
# split questions route into questions and answers
# questions should use GET that renders the question HTML
# which has a form that contains a POST method to /answer route.
# logic that checks survey progress should be handled in /questions
# logic that directs completed user survey should be handled in /answer
