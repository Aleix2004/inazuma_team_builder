from flask import Flask, render_template, redirect, url_for, session, request
import json, os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ------------------ Funciones de utilidad ------------------

def load_players():
    with open("data/players.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_team(team):
    with open("data/team_saved.json", "w", encoding="utf-8") as f:
        json.dump(team, f, ensure_ascii=False, indent=2)

def load_team():
    if os.path.exists("data/team_saved.json"):
        with open("data/team_saved.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def calculate_stats(team):
    if not team:
        return {"ataque": 0, "defensa": 0, "tecnica": 0, "resistencia": 0}

    total = {"ataque": 0, "defensa": 0, "tecnica": 0, "resistencia": 0}
    for p in team:
        total["ataque"] += p.get("ataque", 0)
        total["defensa"] += p.get("defensa", 0)
        total["tecnica"] += p.get("técnica", 0)
        total["resistencia"] += p.get("resistencia", 0)

    n = len(team)
    return {
        "ataque": round(total["ataque"] / n, 1),
        "defensa": round(total["defensa"] / n, 1),
        "tecnica": round(total["tecnica"] / n, 1),
        "resistencia": round(total["resistencia"] / n, 1)
    }

# ------------------ Página principal ------------------

@app.route("/")
def index():
    players = load_players()
    team = session.get("team", load_team())
    stats = calculate_stats(team)
    return render_template("index.html", players=players, team=team, stats=stats)

# ------------------ Explorar jugadores ------------------

@app.route("/explore")
def explore_players():
    players = load_players()
    team = session.get("team", load_team())
    return render_template("explore.html", players=players, team=team)

# ------------------ Añadir jugador ------------------

@app.route("/add/<nombre>")
def add_to_team(nombre):
    players = load_players()
    team = session.get("team", load_team())

    if len(team) >= 11:
        return redirect(url_for("team_view"))

    player = next((p for p in players if p["nombre"] == nombre), None)
    if player and player not in team:
        team.append(player)
        session["team"] = team
        save_team(team)

    return redirect(url_for("explore_players"))

# ------------------ Quitar jugador ------------------

@app.route("/remove/<nombre>")
def remove_from_team(nombre):
    team = session.get("team", load_team())
    team = [p for p in team if p["nombre"] != nombre]
    session["team"] = team
    save_team(team)
    return redirect(url_for("team_view"))

# ------------------ Ver equipo ------------------

@app.route("/team")
def team_view():
    team = session.get("team", load_team())
    stats = calculate_stats(team)
    return render_template("team.html", team=team, stats=stats)

# ------------------ Ver y cambiar formación ------------------

@app.route("/formation", methods=["GET", "POST"])
def formation_view():
    team = session.get("team", load_team())
    formations = ["4-4-2", "4-3-3", "3-5-2", "5-3-2"]

    if request.method == "POST":
        new_formation = request.form.get("formation")
        if new_formation in formations:
            session["formation"] = new_formation
            return redirect(url_for("formation_view"))

    formation = session.get("formation", "4-4-2")
    return render_template("formation.html", team=team, formation=formation, formations=formations)

# ------------------ Ejecutar ------------------

if __name__ == "__main__":
    app.run(debug=True)
