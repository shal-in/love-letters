from flask import Flask, render_template, redirect
import os

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/coming-soon")

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")

# Catch-all route to redirect everything else to /coming-soon
@app.route("/<path:path>")
def catch_all(path):
    return redirect("/coming-soon")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
