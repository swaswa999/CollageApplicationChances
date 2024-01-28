#main PYTHON FILE FOR FLASK
import os
from flask import Flask,render_template, redirect, request
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

@app.route('/application')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 81))
    app.run(host=host, port=port, debug=True)
