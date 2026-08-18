from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import ask_agent


app = Flask(__name__)

CORS(app)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Question cannot be empty."
        }), 400

    try:

        answer = ask_agent(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "error": "Something went wrong while processing your question."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)