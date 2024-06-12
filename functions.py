import json
import os

def load_history():
    history_path = 'historico.json'
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            os.remove(history_path)  # Delete the corrupt file
            return {}  # Return an empty dictionary if the file is corrupt
    return {}
def save_history(data):
    with open('historico.json', 'w') as file:
        json.dump(data, file, indent=4)     

def remove_old_games_from_history(data):
    for team_id in list(data.keys()):
        data[team_id]['response'] = [game for game in data[team_id]['response'] if game['fixture']['status']['elapsed'] is None or game['fixture']['status']['elapsed'] > 70]
    save_history(data)
