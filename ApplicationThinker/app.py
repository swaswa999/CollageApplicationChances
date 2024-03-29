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
    state TEXT,
    citizenship TEXT,
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

    return render_template('index.html')


@app.route('/success/<fname>')
def success(fname):

    try:
        cursor.execute("SELECT * FROM applications")
        print("\033[H\033[J", end="")
        recently_added_record = cursor.fetchone()
        print(recently_added_record)

        internships = (int(recently_added_record[4]) ** 2) / (5 ** 2) * 10
        competitions = (int(recently_added_record[5]) ** 2) / (10 ** 2) * 10
        clubs_participated = (int(recently_added_record[18]) ** 2) / (10 ** 2) * 10

        if recently_added_record[22] != "":
            arts_participation = 10
        else:
            arts_participation = 0

        student_council = recently_added_record[20]
        if student_council == "member":
            student_council = 4
        elif student_council == "vicePresident":
            student_council = 7
        elif student_council == "president":
            student_council = 10
        else:
            student_council = 1

        clubs_participated = (clubs_participated ** 2) / (10 ** 2) * 10

        clubs_led = (int(recently_added_record[19]) ** 2) / (5 ** 2) * 10
        leadership = int(recently_added_record[6] ** 2 / (15 ** 2) * 10)
        citizenship = recently_added_record[8]

        financial_aid = recently_added_record[10]
        if financial_aid == "no":
            financial_aid = 5
        else:
            financial_aid = 9  # Adjusted weight for 'yes'

        household_income = int(recently_added_record[9])
        if household_income <= 50000:
            household_income = 3
        elif 50001 <= household_income <= 85000:
            household_income = 5
        elif 85001 <= household_income <= 100000:
            household_income = 7
        elif 100001 <= household_income <= 125000:
            household_income = 9
        else:
            household_income = 10

        valedictorian = int(recently_added_record[21])
        if valedictorian != "":
            valedictorian = 10
        else:
            valedictorian = 0

        volunteer_hours = recently_added_record[17]
        if volunteer_hours == 'low':
            volunteer_hours = 2
        elif volunteer_hours == 'medium':
            volunteer_hours = 5
        elif volunteer_hours == 'high':
            volunteer_hours = 7
        elif volunteer_hours == 'extremelyHigh':
            volunteer_hours = 10

        sports_participation = recently_added_record[16]

        if sports_participation == "none":
            sports_participation = 1
        elif sports_participation == "provincial":
            sports_participation = 3
        elif sports_participation == "state":
            sports_participation = 5
        elif sports_participation == "national":
            sports_participation = 8
        elif sports_participation == "international":
            sports_participation = 10

        sat_scores = (int(recently_added_record[13]) / 1600) * 10

        currentPercentag = sat_scores * 10

        act_scores = (int(recently_added_record[14]) / 36) * 10
        ap_courses = (int(recently_added_record[15]) / 38) * 10
        unweighted_gpa = (float(recently_added_record[12]) / 4.0) * 10
        weighted_gpa = (float(recently_added_record[11])) / 5.0 * 10
        portfolio = recently_added_record[23]
        if portfolio == "yes":
            portfolio = 10
        else:
            portfolio = 0

        legacy = recently_added_record[3]
        if legacy == "yes":
            legacy = 3
        else:
            legacy = 1

        state = recently_added_record[7]

        if state == "outOfUSA" and citizenship == "noCitizen":
            currentPercentage = 0.000085  # 14%
        elif state == "california" and citizenship == "yesCitizen":
            currentPercentage = 0.00639  # 36%
        else:
            currentPercentage = 0.000231  # 64%

        # currentPercentage = 0.001775 #56,378 applications

        currentPercentage += internships * 5
        currentPercentage += competitions * 5
        currentPercentage += clubs_participated * 2
        currentPercentage += arts_participation * 2
        currentPercentage += clubs_led * 4
        currentPercentage += leadership * 4
        currentPercentage += financial_aid * 3
        currentPercentage += household_income * 3
        currentPercentage += sports_participation * 5
        currentPercentage += sat_scores * 5
        currentPercentage += act_scores * 4
        currentPercentage += ap_courses * 4
        currentPercentage += unweighted_gpa * 4
        currentPercentage += weighted_gpa * 5
        currentPercentage += legacy * 4
        currentPercentage += valedictorian * 4  # Added weight for valedictorian
        currentPercentage += volunteer_hours * 3  # Added weight for volunteer hours
        currentPercentage += student_council * 2  # Added weight for student council
        currentPercentage += portfolio * 2  # Added weight for portfolio

        currentPercentage /= 9  # Adjusted the denominator for added factors

        currentPercentage = round(currentPercentage, 2)
        conn.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('error.html')

    return render_template('success.html', fname=fname,currentPercentage=currentPercentage )

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 81))
    app.run(host=host, port=port, debug=True) #REMEMBER TO CHANGE TO FALSE LATER
