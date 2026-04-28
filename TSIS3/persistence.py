import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            if "color" not in data:
                data["color"] = "BLUE"
            return data
    return {"sound": True, "color": "BLUE", "difficulty": "Medium"}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f: json.dump(settings, f, indent=4)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f: return json.load(f)
    return []

def save_score(name, score):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score})
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f: json.dump(lb, f, indent=4)