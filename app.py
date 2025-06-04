from flask import Flask, render_template, request, jsonify
import re
import random
import string

app = Flask(__name__)

def check_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ @!#$%^&*()<>?/\\|}{~:]", password) is None
    errors = {
        'length': length_error,
        'digit': digit_error,
        'uppercase': uppercase_error,
        'lowercase': lowercase_error,
        'symbol': symbol_error
    }
    score = 5 - sum(errors.values())

    if score <= 2:
        strength = "Weak"
    elif score == 3 or score == 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    missing = [k for k, v in errors.items() if v]
    return strength, score, missing

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data['password']
    strength, score, missing = check_strength(password)

    tips_map = {
        'length': 'Make it at least 8 characters long.',
        'digit': 'Add at least one number.',
        'uppercase': 'Include uppercase letters.',
        'lowercase': 'Include lowercase letters.',
        'symbol': 'Use special characters like !, @, #, etc.'
    }

    tips = [tips_map[key] for key in missing]
    return jsonify({'strength': strength, 'score': score, 'tips': tips})

@app.route('/suggest_password', methods=['GET'])
def suggest_password_route():
    length = int(request.args.get('length', 12))
    password = generate_password(length)
    return jsonify({'suggestion': password})

if __name__ == '__main__':
    app.run(debug=True)
