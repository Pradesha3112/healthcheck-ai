from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route('/')
def select_mode():
    return render_template('mode_select.html')

@app.route('/normal', methods=['GET', 'POST'])
def normal_mode():
    report = None
    if request.method == 'POST':
        try:
            heart_rate = int(request.form['heart_rate'])
            temperature = float(request.form['temperature'])
            oxygen = int(request.form['oxygen'])

            messages = []

            if heart_rate < 60:
                messages.append("🫀 Heart rate is low. Possible fatigue or bradycardia.")
            elif heart_rate > 100:
                messages.append("🫀 Heart rate is high. Possible stress or cardiovascular strain.")

            if temperature < 97.0:
                messages.append("🌡️ Temperature is low. Could be due to hypothyroidism or cold.")
            elif temperature > 99.5:
                messages.append("🌡️ You have a fever. Possible infection or inflammation.")

            if oxygen < 95:
                messages.append("🫁 Oxygen level is low. May indicate breathing issues.")

            if not messages:
                report = "✅ All your vital signs are within a healthy range. Stay healthy!"
            else:
                report = "🧠 <strong>Health Summary:</strong><br>" + "<br>".join(messages) + "<br><br>🩺 Please consult a doctor."

        except ValueError:
            report = "⚠️ Invalid input. Please enter numbers only."

    return render_template('index.html', result=report)

@app.route('/chatbot')
def chatbot_mode():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message'].lower()

    heart_match = re.search(r'heart.*?(\d+)', user_input)
    temp_match = re.search(r'temp.*?(\d+\.?\d*)', user_input)
    oxy_match = re.search(r'oxygen.*?(\d+)', user_input)

    heart = int(heart_match.group(1)) if heart_match else None
    temp = float(temp_match.group(1)) if temp_match else None
    oxy = int(oxy_match.group(1)) if oxy_match else None

    messages = []

    if heart:
        if heart < 60:
            messages.append("🫀 Heart rate is low.")
        elif heart > 100:
            messages.append("🫀 Heart rate is high.")

    if temp:
        if temp < 97:
            messages.append("🌡️ Temperature is low.")
        elif temp > 99.5:
            messages.append("🌡️ High temperature.")

    if oxy and oxy < 95:
        messages.append("🫁 Oxygen level is low.")

    if not messages:
        reply = "✅ All vitals are normal. You're good to go!"
    else:
        reply = "<br>".join(messages) + "<br>🩺 Please consult a doctor if symptoms persist."

    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(debug=True)
