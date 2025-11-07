from flask import Flask, render_template, jsonify, request, url_for, redirect
import json
import os

app = Flask(__name__)

# Archivos dentro de /data
DATA_DIR = "data"
PLAYERS_FILE = os.path.join(DATA_DIR, "players.json")
TEAM_FILE = os.path.join(DATA_DIR, "team_saved.json")

# --- Cargar jugadores ---
def load_players():
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Guardar equipo ---
def save_team_data(team, formation):
    with open(TEAM_FILE, "w", encoding="utf-8") as f:
        json.dump({"team": team, "formation": formation}, f, ensure_ascii=False, indent=2)

# --- Cargar equipo ---
def load_team_data():
    if not os.path.exists(TEAM_FILE):
        return [], "4-4-2"
    with open(TEAM_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return data, "4-4-2"
        return data.get("team", []), data.get("formation", "4-4-2")

# --- Calcular estadísticas ---
def calculate_team_stats(team):
    if not team:
        return {"ataque": 0, "defensa": 0, "tecnica": 0, "resistencia": 0}
    total = {"ataque": 0, "defensa": 0, "tecnica": 0, "resistencia": 0}
    for player in team:
        total["ataque"] += player.get("ataque", 0)
        total["defensa"] += player.get("defensa", 0)
        total["tecnica"] += player.get("técnica", 0)
        total["resistencia"] += player.get("resistencia", 0)
    n = len(team)
    return {k: round(v / n, 1) for k, v in total.items()}

# --- Página principal ---
@app.route("/")
def index():
    players = load_players()
    team, formation = load_team_data()
    stats = calculate_team_stats(team)
    return render_template("index.html", players=players, team=team, formation=formation, stats=stats)

# --- Ver equipo actual ---
@app.route("/team")
def team_view():
    team, formation = load_team_data()
    avg = calculate_team_stats(team)
    return render_template("team.html", team=team, avg=avg)

# --- Añadir jugador al equipo ---
@app.route("/add_to_team/<nombre>")
def add_to_team(nombre):
    players = load_players()
    team, formation = load_team_data()

    if any(p["nombre"] == nombre for p in team):
        return redirect(url_for("team_view"))

    if len(team) >= 11:
        return redirect(url_for("team_view"))

    player = next((p for p in players if p["nombre"] == nombre), None)
    if player:
        team.append(player)
        save_team_data(team, formation)

    return redirect(url_for("team_view"))

# --- Quitar jugador ---
@app.route("/remove_from_team/<nombre>")
def remove_from_team(nombre):
    team, formation = load_team_data()
    team = [p for p in team if p["nombre"] != nombre]
    save_team_data(team, formation)
    return redirect(url_for("team_view"))

# --- Guardar equipo desde JS ---
@app.route("/save_team", methods=["POST"])
def save_team():
    data = request.get_json()
    team = data.get("team", [])
    formation = data.get("formation", "4-4-2")
    save_team_data(team, formation)
    stats = calculate_team_stats(team)
    return jsonify({"success": True, "stats": stats})

# --- Explorar jugadores ---
@app.route("/explore")
def explore_players():
    players = load_players()
    team, _ = load_team_data()
    team_names = [p["nombre"] for p in team]
    return render_template("explore.html", players=players, team_names=team_names)

# --- Ver y cambiar formación ---
@app.route("/formation", methods=["GET", "POST"])
def formation_view():
    team, formation = load_team_data()
    formations = ["4-4-2", "4-3-3", "3-5-2", "5-3-2"]

    if request.method == "POST":
        new_formation = request.form.get("formation", formation)
        save_team_data(team, new_formation)
        formation = new_formation

    return render_template("formation.html", team=team, formation=formation, formations=formations)

# --- Reiniciar equipo ---
@app.route("/reset_team")
def reset_team():
    save_team_data([], "4-4-2")
    return redirect(url_for("team_view"))

if __name__ == "__main__":
    app.run(debug=True)
