import json
from core.team import Team


def load_players(path="data/players.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de jugadores.")
        return []


def main():
    players = load_players()
    if not players:
        return

    team = Team(players)

    while True:
        print("\n=== Inazuma Team Builder ===")
        print("1. Ver jugadores disponibles")
        print("2. Añadir jugador al equipo")
        print("3. Ver mi equipo")
        print("4. Calcular estadísticas del equipo")
        print("5. Guardar equipo")
        print("0. Salir")

        choice = input("Elige una opción: ")

        if choice == "1":
            team.show_players()
        elif choice == "2":
            try:
                index = int(input("Número del jugador: "))
                team.add_player(index)
            except ValueError:
                print("❌ Ingresa un número válido.")
        elif choice == "3":
            team.show_team()
        elif choice == "4":
            team.calculate_stats()
        elif choice == "5":
            team.save_team()
        elif choice == "0":
            print("👋 Saliendo del programa...")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    main()
