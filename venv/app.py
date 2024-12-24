from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import time

app = Flask(__name__)
key = Fernet.generate_key()
cipher_suite = Fernet(key)
capsules = {}

@app.route('/create', methods=['POST'])
def create_capsule():
    data = request.json
    message = data['message']
    unlock_time = data['unlock_time']
    capsule_id = str(len(capsules) + 1)
    encrypted_message = cipher_suite.encrypt(message.encode())
    capsules[capsule_id] = {"message": encrypted_message, "unlock_time": unlock_time}
    return jsonify({"id": capsule_id})

@app.route('/get/<capsule_id>', methods=['GET'])
def get_capsule(capsule_id):
    capsule = capsules.get(capsule_id)
    if not capsule:
        return jsonify({"error": "Capsule not found"}), 404

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    if current_time < capsule["unlock_time"]:
        return jsonify({"time_remaining": capsule["unlock_time"]})

    decrypted_message = cipher_suite.decrypt(capsule["message"]).decode()
    return jsonify({"message": decrypted_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
