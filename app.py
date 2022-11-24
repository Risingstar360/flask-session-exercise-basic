from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES = "responses"

app=Flask(__name__)
app.config['SECRET_KEY'] = "martin_norris200"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """home page - intro and start button for survey"""
    return render_template("home.html", survey = survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """clear the session of all responses"""
    session[RESPONSES] = []

    return redirect("/questions/0")

@app.route("/answer", methods= ["POST"])
def answer_questions():
    choice = request.form["answer"]
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/finished")

    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Displays current question."""
    responses = session.get(RESPONSES)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Incorrect question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)

@app.route("/finished")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")


