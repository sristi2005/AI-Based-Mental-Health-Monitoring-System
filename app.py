from flask import Flask, request, render_template, jsonify, url_for, redirect
import pickle
import pandas as pd
from database import get_db


# ----------------- RULE BASED SENTIMENT -----------------

NEGATIVE_WORDS = {
    "sad": 2,
    "depressed": 4,
    "lonely": 3,
    "anxious": 3,
    "tired": 2,
    "hopeless": 4,
    "stressed": 3,
    "worried": 2,
    "overwhelmed": 3,
    "empty": 3,
    "angry": 2
}

POSITIVE_WORDS = {
    "happy": -3,
    "relaxed": -2,
    "calm": -2,
    "good": -1,
    "peaceful": -2,
    "excited": -1,
    "fine": -1,
    "okay": -1
}

# Load your trained stress model
with open('model/stress_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__, template_folder='templates')

@app.route('/')
def landing():
    return render_template('main.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        country = request.form['country']

        print(name, email, age, country)

        return redirect(url_for('dashboard'))

    return render_template('form.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        answers = []
        for i in range(1, 11):
            answers.append(int(request.form[f'q{i}']))

        score = sum(answers)

        if score <= 4:
            result = "Minimal Depression"
        elif score <= 9:
            result = "Mild Depression"
        elif score <= 14:
            result = "Moderate Depression"
        elif score <= 19:
            result = "Moderately Severe Depression"
        else:
            result = "Severe Depression"

        return render_template('result.html', result=result)
    return render_template('test.html')

@app.route("/anxiety_test", methods=['GET', 'POST'])
def anxiety_test():
    if request.method == 'POST':
        scores = []

        for i in range(1, 8):
            value = request.form.get(f"q{i}")

            if value is None:
                # safety fallback (should not happen if HTML is correct)
                return "Please answer all questions", 400

            scores.append(int(value))

        total_score = sum(scores)

        if total_score <= 4:
            result = "Minimal Anxiety"
        elif total_score <= 9:
            result = "Mild Anxiety"
        elif total_score <= 14:
            result = "Moderate Anxiety"
        else:
            result = "Severe Anxiety"

        return render_template(
            "anxiety_result.html",
            result=result
        )

    return render_template('anxiety_test.html')



# ----------------- STRESS PREDICTION API -----------------

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    session_duration = float(data["session_duration"])
    typing_delay     = float(data["typing_delay"])
    click_rate       = float(data["click_rate"])
    checkin_score    = float(data["checkin_score"])

    features = [[session_duration, typing_delay, click_rate, checkin_score]]

    prediction = model.predict(features)[0]

    return jsonify({"stress_level": int(prediction)})


# ----------------- CHECK-IN FORM -----------------

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'GET':
        return render_template('checkin.html')

    # --------- AUTO CAPTURED BEHAVIOR ----------
    session_duration = float(request.form['session_duration'])
    typing_delay = float(request.form['typing_delay'])
    click_rate = float(request.form['click_rate'])
    checkin_score = float(request.form['checkin_score'])

    # --------- TEXT ANALYSIS ----------
    text = request.form.get("thoughts", "").lower()
    words = text.split()

    sentiment_score = 0

    for word in words:
        if word in NEGATIVE_WORDS:
            sentiment_score += NEGATIVE_WORDS[word]
        if word in POSITIVE_WORDS:
            sentiment_score += POSITIVE_WORDS[word]

    # --------- COMBINE BOTH ----------
    final_score = (
        sentiment_score +
        (typing_delay / 300) +
        (click_rate * 2) +
        checkin_score
    )

    # --------- MAP TO STRESS LEVEL ----------
    if final_score <= 2:
        stress_level_text = "Low Stress"
        stress_level_num = 1
    elif final_score <= 6:
        stress_level_text = "Moderate Stress"
        stress_level_num = 2
    else:
        stress_level_text = "High Stress"
        stress_level_num = 3
    db = get_db()
    db.execute(
    "INSERT INTO checkins (stress_level) VALUES (?)",
    (stress_level_num,)
    ) 
    db.commit()
    db.close()


    return render_template(
        "message.html",
        stress_level=stress_level_text
    )

@app.route("/weekly-data")
def weekly_data():
    db = get_db()
    rows = db.execute("""
        SELECT created_at, AVG(stress_level) as avg_stress
        FROM checkins
        WHERE created_at >= date('now','-6 days')
        GROUP BY created_at
        ORDER BY created_at
    """).fetchall()
    db.close()

    labels = [row["created_at"] for row in rows]
    values = [round(row["avg_stress"], 2) for row in rows]

    return jsonify({
        "labels": labels,
        "values": values
    })


# ----------------- MAIN -----------------

if __name__ == "__main__":
    app.run(debug=True)