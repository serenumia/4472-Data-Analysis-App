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

    url = f"https://www.thebluealliance.com/api/v3/team/frc4472/event/{event_code}/matches/simple"

    headers = {
        "X-TBA-Auth-Key": api_key
    }

    response = requests.get(url, headers=headers)

    matches = response.json()

    qm_matches = []
    for match in matches:
        if match["comp_level"] == "qm":
            qm_matches.append(match)

    sf_matches = []
    for match in matches:
        if match["comp_level"] == "sf":
            sf_matches.append(match)

    f_matches = []
    for match in matches:
        if match["comp_level"] == "f":
            f_matches.append(match)

    return render_template('event.html', quali_matches=qm_matches, semifinal_matches=sf_matches, final_matches=f_matches)


if __name__ == '__main__':
    app.run(debug=True)