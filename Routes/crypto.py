from flask import Flask, render_template
from symmetric import symmetric_bp

app = Flask(__name__, template_folder="../templates")

# register symmetric routes
app.register_blueprint(symmetric_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)