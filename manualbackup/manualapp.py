from flask import Flask, render_template, request
import requests
import os 
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home2():
    return render_template('home2.html')

@app.route("/event2")
def event2():
    event2_code = request.args.get("event_code")

    match_number= request.args.get("match_number")

    api_key = os.environ.get("TBA_API_KEY")

    url = f"https://www.thebluealliance.com/api/v3/event/{event2_code}/{match_number}/simple"

    headers = {
        "X-TBA-Auth-Key": api_key
    }

    response = requests.get(url, headers=headers)

    matches = response.json()


    qm_matches = []
    for match in matches:
        if match["comp_level"] == "qm":
            qm_matches.append(match)

    return render_template('event2.html')


if __name__ == '__main__':
    app.run(debug=True)