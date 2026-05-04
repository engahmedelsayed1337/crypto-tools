from flask import Flask, render_template, request
from symmetric import symmetric_bp
import asymmetric
import importlib
importlib.reload(asymmetric)
app = Flask(__name__, template_folder="../templates")

# register symmetric routes
app.register_blueprint(symmetric_bp)

@app.route("/")
def home():
    return render_template("index.html")
# ───────── ASYMMETRIC ROUTES ─────────

@app.route('/api/asymmetric/generate-keys', methods=['POST'])
def generate_keys_route():
    public_key, private_key = asymmetric.generate_keys()
    return {
        "public_key": public_key,
        "private_key": private_key
    }


@app.route('/api/asymmetric/encrypt', methods=['POST'])
def encrypt_rsa_route():
    data = request.get_json()

    message = data.get("message")
    public_key = data.get("public_key")

    if not message or not public_key:
        return {"error": "Missing data"}, 400

    result = asymmetric.encrypt_rsa(message, public_key)
    return {"result": result}


@app.route('/api/asymmetric/decrypt', methods=['POST'])
def decrypt_rsa_route():
    data = request.get_json()

    ciphertext = data.get("ciphertext")
    private_key = data.get("private_key")

    if not ciphertext or not private_key:
        return {"error": "Missing data"}, 400

    result = asymmetric.decrypt_rsa(ciphertext, private_key)
    return {"result": result}
if __name__ == "__main__":
    app.run(debug=True)