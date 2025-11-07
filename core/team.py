import json
from typing import List, Dict


class Team:
    def __init__(self, players: List[Dict]):
        self.players = players
        self.team = []

    def show_players(self):
        print("\n--- Jugadores disponibles ---")
        for i, p in enumerate(self.players, start=1):
            print(f"{i}. {p['nombre']} - {p['posición']} "
                  f"(Ataque:{p['ataque']}, Defensa:{p['defensa']}, "
                  f"Técnica:{p['técnica']}, Resistencia:{p['resistencia']})")

    def add_player(self, index: int):
        if len(self.team) >= 11:
            print("⚠️ El equipo ya tiene 11 jugadores.")
            return
        try:
            player = self.players[index - 1]
            if player in self.team:
                print("⚠️ Ese jugador ya está en tu equipo.")
                return
            self.team.append(player)
            print(f"✅ {player['nombre']} añadido al equipo.")
        except IndexError:
            print("❌ Número inválido.")

    def show_team(self):
        if not self.team:
            print("\nAún no hay jugadores en el equipo.")
            return
        print("\n=== Tu equipo actual ===")
        for p in self.team:
            print(f"- {p['nombre']} ({p['posición']})")

    def calculate_stats(self):
        if not self.team:
            print("\n❌ No hay jugadores en el equipo.")
            return
        total = {"ataque": 0, "defensa": 0, "técnica": 0, "resistencia": 0}
        for p in self.team:
            total["ataque"] += p["ataque"]
            total["defensa"] += p["defensa"]
            total["técnica"] += p["técnica"]
            total["resistencia"] += p["resistencia"]

        avg = {k: v / len(self.team) for k, v in total.items()}

        print("\n--- Estadísticas del equipo ---")
        for stat, val in avg.items():
            print(f"{stat.capitalize()}: {val:.1f}")

        return avg

    def save_team(self, filename="data/team_saved.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.team, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Equipo guardado en {filename}")
