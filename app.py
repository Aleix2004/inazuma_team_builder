from flask import Flask, render_template, redirect, url_for, session, request
import json, os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ------------------ Cargar jugadores ------------------
def load_players():
    with open("data/players.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------ Estadísticas ------------------
def calculate_stats(team):
    if not team:
        return {"ataque": 0, "defensa": 0, "tecnica": 0, "resistencia": 0}
    n = len(team)
    return {
        "ataque": round(sum(p["ataque"] for p in team)/n, 1),
        "defensa": round(sum(p["defensa"] for p in team)/n, 1),
        "tecnica": round(sum(p["técnica"] for p in team)/n, 1),
        "resistencia": round(sum(p["resistencia"] for p in team)/n, 1),
    }

# ------------------ Página principal ------------------
@app.route("/")
def index():
    if "team" not in session:
        session["team"] = []
    players = load_players()
    team = session["team"]
    stats = calculate_stats(team)
    return render_template("index.html", players=players, team=team, stats=stats)

# ------------------ Explorar jugadores ------------------
@app.route("/explore")
def explore_players():
    if "team" not in session:
        session["team"] = []
    players = load_players()
    team = session["team"]
    return render_template("explore.html", players=players, team=team)

# ------------------ Añadir jugador ------------------
@app.route("/add/<nombre>")
def add_to_team(nombre):
    if "team" not in session:
        session["team"] = []
    team = session["team"]
    players = load_players()

    if len(team) >= 11:
        return redirect(url_for("team_view"))

    player = next((p for p in players if p["nombre"] == nombre), None)
    if player and player not in team:
        team.append(player)
        session["team"] = team
    return redirect(url_for("explore_players"))

# ------------------ Quitar jugador ------------------
@app.route("/remove/<nombre>")
def remove_from_team(nombre):
    if "team" not in session:
        session["team"] = []
    team = session["team"]
    team = [p for p in team if p["nombre"] != nombre]
    session["team"] = team
    return redirect(url_for("team_view"))

# ------------------ Ver equipo ------------------
@app.route("/team")
def team_view():
    if "team" not in session:
        session["team"] = []
    team = session["team"]
    stats = calculate_stats(team)
    return render_template("team.html", team=team, avg=stats)

# ------------------ Ver formación ------------------
@app.route("/formation", methods=["GET", "POST"])
def formation_view():
    if "team" not in session:
        session["team"] = []
    team = session["team"]

    # Definir formaciones disponibles
    formations = ["4-4-2", "4-3-3", "3-5-2", "5-3-2"]
    if "formation" not in session:
        session["formation"] = "4-4-2"

    if request.method == "POST":
        new_formation = request.form.get("formation")
        if new_formation in formations:
            session["formation"] = new_formation

    return render_template(
        "formation.html",
        team=team,
        formation=session["formation"],
        formations=formations
    )

# ------------------ Resetear equipo ------------------
@app.route("/reset_team")
def reset_team():
    session["team"] = []
    session["formation"] = "4-4-2"
    return redirect(url_for("index"))

# ------------------ Ejecutar ------------------
if __name__ == "__main__":
    app.run(debug=True)
