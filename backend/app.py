from flask import Flask, request, jsonify
from openai_assistant import send_message

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_message = data.get('message')

    assistant_response = send_message(user_message)
    
    return jsonify({"response": assistant_response or "No response from assistant."})

if __name__ == '__main__':
    app.run(debug=True)
