#main PYTHON FILE FOR FLASK
import os
from flask import Flask,render_template, redirect, request, url_for
import sqlite3

conn = sqlite3.connect('collageapplications.db', check_same_thread=False)
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
    state TEXT,  -- or state_code TEXT
    citizenship TEXT,  -- or citizenship_code TEXT
    householdIncome INTEGER,
    financialAid TEXT,
    weightedGPA REAL,
    unweightedGPA REAL,
    satScores INTEGER,
    actScores INTEGER,
    apCourses INTEGER,
    sportsParticipation TEXT,
    volunteerHours TEXT,
    clubsParticipated INTEGER,
    clubsLed INTEGER,
    studentCouncil INTEGER,
    valedictorian INTEGER,
    artsParticipation INTEGER,
    portfolio TEXT
)"""

cursor.execute(create_table_query)
conn.commit()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/application', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('collageapplications.db', check_same_thread=False)
    cursor = conn.cursor()

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
            householdIncome = int(request.form.get('HouseholdIncome'))
            financialAid = request.form.get('financialAid')
            weightedGPA = float(request.form.get('weightedGPA'))
            unweightedGPA = float(request.form.get('unweightedGPA'))
            satScores = int(request.form.get('satScores'))
            actScores = int(request.form.get('actScores'))
            apCourses = int(request.form.get('apCourses'))
            sportsParticipation = request.form.get('sportsParticipation')
            volunteerHours = request.form.get('volunteerHours')
            clubsParticipated = int(request.form.get('clubsParticipated'))
            clubsLed = int(request.form.get('clubsLed'))
            studentCouncil = request.form.get('studentCouncil')
            valedictorian = int(request.form.get('valedictorian')) #CHECK FOR MUL
            artsParticipation = request.form.get('artsParticipation') #CHECK FOR MULTIOUTPUT
            portfolio = request.form.get('portfolio')

            try:
                cursor.execute(f"INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (fname, lname, age, legacy, internships, competitions, leadership, state, citizenship, householdIncome, financialAid, weightedGPA, unweightedGPA,satScores, actScores, apCourses, sportsParticipation, volunteerHours, clubsParticipated, clubsLed, studentCouncil, valedictorian, artsParticipation, portfolio))
                conn.commit()
                return redirect(url_for('success', fname=fname))
            except Exception as e:
                print(f"Error inserting data: {str(e)}")
                return render_template('error.html')

        except Exception as e:
            print(f"Error: {str(e)}")
            return render_template('error.html')

        finally:
            conn.close()

    return render_template('index.html')


@app.route('/success/<fname>')
def success(fname):

    try:
        cursor.execute("SELECT * FROM applications")
        print("\033[H\033[J", end="")
        recently_added_record = cursor.fetchone()
        print(recently_added_record)

        internships = (int(recently_added_record[4]) ** 2) / (4 ** 2) * 10
        competitions = (int(recently_added_record[5]) ** 2) / (10 ** 2) * 10
        clubs_participated = (int(recently_added_record[18]) ** 2) / (5 ** 2) * 10

        if  recently_added_record[22] != "":
            arts_participation =  10

        student_council = recently_added_record[20]
        if student_council == "member":
            student_council =  2
        elif student_council == "vicePresident":
            student_council =  7
        elif student_council == "president":
            student_council =  10
        elif student_council == "no":
            student_council =  0

        clubs_participated =  (clubs_participated ** 2) / (10 ** 2) *10

        clubs_led = (int(recently_added_record[19])**3) / (3**2) *10
        leadership = int(recently_added_record[6]**3 / (3**2) *10)
        citizenship = recently_added_record[8]

        financial_aid = recently_added_record[10]
        if financial_aid == "no":
            financial_aid =  5

        household_income = int(recently_added_record[9])
        valedictorian = int(recently_added_record[21])
        volunteer_hours = recently_added_record[17]
        sports_participation = recently_added_record[16]
        sat_scores = int(recently_added_record[13])
        act_scores = int(recently_added_record[14])
        ap_courses = int(recently_added_record[15])
        unweighted_gpa = float(recently_added_record[12])
        weighted_gpa = float(recently_added_record[11])
        portfolio = recently_added_record[23]

        legacy = recently_added_record[3]
        if legacy == "yes":
            legacy = 3
        else:
            legacy = 0
    

        state = recently_added_record[7]

        if state ==  "outOfUSA" and citizenship == "noCitizen":
            currentPercentage =  0.0000085 #14%
        elif state == "california" and citizenship == "yesCitizen":
            currentPercentage = 0.000639 # 36%
        else:
            currentPercentage = 0.0000231 # 64%


        #currentPercentage = 0.001775 #56,378 applications
        currentPercentage *=  internships
        currentPercentage *=  competitions
        currentPercentage *=  clubs_participated
        currentPercentage *=  arts_participation
        currentPercentage *=  clubs_led
        currentPercentage *=  leadership
        currentPercentage *= financial_aid


        currentPercentage *= 3





        conn.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('error.html')
    finally:
        conn.close()

    return render_template('success.html', fname=fname,)

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 81))
    app.run(host=host, port=port, debug=True) #REMEMBER TO CHANGE TO FALSE LATER
