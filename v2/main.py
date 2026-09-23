from flask import Flask, render_template, request
import requests
import os 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/event")
def event():
    event_code = request.args.get("event_code")

    api_key = os.environ.get("TBA_API_KEY")

    url = f"https://www.thebluealliance.com/api/v3/event/{event_code}/matches"

    headers = {
        "X-TBA-Auth-Key": api_key
    }

    response = requests.get(url, headers=headers)

    matches = response.json()

    return render_template(
        "event.html",
        matches=matches
    )

if __name__ == '__main__':
    app.run(debug=True)