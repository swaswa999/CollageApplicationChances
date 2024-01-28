#main PYTHON FILE FOR FLASK
import os
from flask import Flask,render_template, redirect, request, url_for
import sqlite3

conn = sqlite3.connect('collageapplications.db')

cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS applications (
    fname TEXT,
    lname TEXT,
    age INTEGER,
    legacy TEXT,
    internships INTEGER,
    competitions INTEGER,
    leadership INTEGER,
    state TEXT,
    citizenship TEXT,
    HouseholdIncome INTEGER,
    financialAid TEXT,
    weightedGPA REAL,
    Unweighted REAL,
    satScores INTEGER,
    actScores INTEGER,
    apCourses INTEGER,
    sportsParticipation TEXT,
    volunteerHours TEXT,
    clubsParticipated INTEGER,
    clubsLed INTEGER,
    studentCouncil TEXT,
    valedictorian INTEGER,
    artsParticipation TEXT,
    portfolio TEXT
)"""

cursor.execute(create_table_query)
conn.commit()
conn.close()


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/application', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            age = int(request.form.get('age'))
            legacy = request.form.get('legacy')
            internships = int(request.form.get('internships'))
            competitions = int(request.form.get('competitions'))
            leadership = int(request.form.get('leadership'))
            state = request.form.get('state')
            citizenship = request.form.get('citizenship')
            household_income = int(request.form.get('HouseholdIncome'))
            weighted_gpa = float(request.form.get('weightedGPA'))
            unweighted_gpa = float(request.form.get('unweightedGPA'))
            sat_scores = int(request.form.get('satScores'))
            act_scores = int(request.form.get('actScores'))
            ap_courses = int(request.form.get('apCourses'))
            sports_participation = request.form.get('sportsParticipation')
            volunteer_hours = request.form.get('volunteerHours')
            clubs_participated = int(request.form.get('clubsParticipated'))
            clubs_led = int(request.form.get('clubsLed'))
            student_council = request.form.get('studentCouncil')
            valedictorian = int(request.form.get('valedictorian')) #CHECK FOR MUL
            arts_participation = request.form.get('artsParticipation') #CHECK FOR MULTIOUTPUT
            portfolio = request.form.get('portfolio')

            return redirect(url_for('success', fname=fname))  # Assuming you have a 'success' endpoint

        except Exception as e:
            print(str(e))
            return render_template('error.html')

    return render_template('index.html')

@app.route('/success/<fname>')
def success(fname):
    return render_template('success.html', fname=fname)



if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 81))
    app.run(host=host, port=port, debug=True)
