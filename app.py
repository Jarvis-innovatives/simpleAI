from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

BRAIN_FILE = "brain.json"

def load_brain():
    with open(BRAIN_FILE, "r") as f:
        return json.load(f)

def save_brain(data):
    with open(BRAIN_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json["message"].lower()
    brain = load_brain()

    if user_text in brain:
        reply = brain[user_text]
    else:
        reply = "I don't know this yet 🤔. Train me!"
    
    return jsonify({"reply": reply})

@app.route("/train", methods=["POST"])
def train():
    data = request.json
    question = data["question"].lower()
    answer = data["answer"]

    brain = load_brain()
    brain[question] = answer
    save_brain(brain)

    return jsonify({"status": "trained"})
    
if __name__ == "__main__":
    app.run(debug=True)
