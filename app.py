from flask import Flask, render_template, redirect, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/coming-soon")

    # return render_template("index.html")


@app.route("/write")
def write():
    return render_template("write.html")

@app.route("/read")
def read():
    # GET RANDOM LETTER ID, redirect to letter id

    letter_id = 1234
    return redirect("/1234")

@app.route("/<letter_id>")
def letter(letter_id):
    # Check if letter_id in db (if not but letter is still a number, redirect to / or /read)
    # get letter from db (HTML thing)
    # Return html (line below)
    # return render_template("letter.html", letter=letter, letter_id=1234)

    print (letter_id)
    return (redirect("/"))
    

@app.route("/coming-soon")
def coming_soon():
    return render_template("coming-soon.html")

# Catch-all route to redirect everything else to /=
@app.route("/<path:path>")
def catch_all(path):
    return redirect("/")


# API
# Write
# Data received looks like:
# {"to": "example TO", "from": "example FROM", "text": "example TEXT"}
@app.route("/api/write", methods=["POST"])
def write_letter():
    raw_data = request.data.decode('utf-8')
    
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
    
    # get next available letter_id

    # convert everything to the html string (write the function for this, example in scrap.ipynb.
    # Look at what the format of the letter is in letter.html (looking for a div with class="letter"))

    # store the html string AND the raw data in db
    
    # return the letter_id (will redirect from frontend)
    
    return jsonify({"message": "Received!", "data": data})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
