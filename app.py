from flask import Flask, render_template, redirect, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/coming-soon")

@app.route("/write")
def write():
    return render_template("write.html")

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")

# Catch-all route to redirect everything else to /coming-soon
@app.route("/<path:path>")
def catch_all(path):
    return redirect("/coming-soon")


# API
# Random letter (maybe something like /random)


# Write
# Data received looks like:
# {"to": "example TO", "from": "example FROM", "text": "example TEXT"}
@app.route("/api/write", methods=["POST"])
def write_letter():
    # Decode the raw data from bytes to string (assuming it's UTF-8 encoded)
    raw_data = request.data.decode('utf-8')
    
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
    
    # CREATE DATABASE ENTRY, THEN RETURN THE REDIRECT OF THE DATABASE ENTRY
    
    return jsonify({"message": "Received!", "data": data})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
