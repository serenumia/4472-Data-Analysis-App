from flask import Flask, render_template, request
import requests
import os 
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
app = Flask(__name__)
team_data = pd.read_excel("data/ICR_DATA.xlsx")

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/event")
def event():
    event_code = request.args.get("event_code")

    match_number= request.args.get("match_number")

    api_key = os.environ.get("TBA_API_KEY")

    url = f"https://www.thebluealliance.com/api/v3/event/{event_code}/{match_number}/simple"

    headers = {
        "X-TBA-Auth-Key": api_key
    }

    response = requests.get(url, headers=headers)

    matches = response.json()
    print(type(matches))
    print(matches)


    for match in matches:
        if match["match_number"] == match_number:
            selected_match = match
            break

    red_teams = selected_match["alliances"]["red"]["team_keys"]

    red_team_data = []
    for team in red_teams:
        team_number = team.replace("frc","")
        data = get_team_data(team_number)
        
        team_info = {
        "team_number": team_number,
        "data": data
        }
        red_team_data.append(team_info)

    blue_teams = selected_match["alliances"]["blue"]["team_keys"]
    blue_team_data = []
    for team in blue_teams:
        team_number = team.replace("frc","")
        data = get_team_data(team_number)

        team_info = {
            "team_number": team_number,
            "data": data
        }
        blue_team_data.append(team_info)

    

    return render_template(
        'event.html', 
        selected_match=selected_match, 
        red_teams=red_team_data, 
        blue_teams=blue_team_data)

def get_team_data(team_number):
    team = team_data[team_data["Team"] == int(team_number)]
    if team.empty: 
        return None

    row = team.iloc[0]
    return {
        "drivetrain": row["drivetrain"],
        "shooter_type": row["shooter type"],
        "hopper_size": row["hopper size"],
        "speed_rating": row["speed rating"],
        "driv_rating": row["2026 driv rating"],
        "accuracy_rating": row["accuracy rating"],
        "sotm": row["SOTM"]
    }

#def get_statbotics_data(team_number):
    #[]

if __name__ == '__main__':
    app.run(debug=True)