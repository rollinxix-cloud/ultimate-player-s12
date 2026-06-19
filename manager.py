import json
import os
import random

# File tracking
JSON_FILE = 'tournament.json'

# Initial structure for a clean tournament
DEFAULT_STATE = {
    "players": [],
    "matches": {
        "qf1": {"p1": None, "p2": None, "winner": None},
        "qf2": {"p1": None, "p2": None, "winner": None},
        "qf3": {"p1": None, "p2": None, "winner": None},
        "qf4": {"p1": None, "p2": None, "winner": None},
        "sf1": {"p1": None, "p2": None, "winner": None},
        "sf2": {"p1": None, "p2": None, "winner": None},
        "final": {"p1": None, "p2": None, "winner": None}
    }
}

def load_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def register_players(data):
    players = data['players']
    if len(players) >= 8:
        print("\n⚠️ Roster is already full!")
        input("Press Enter to return...")
        return

    while len(players) < 8:
        print(f"\nRegistering: {len(players)}/8")
        name = input(f"Enter Player {len(players)+1} Name (or 'q' to stop): ").strip()
        if name.lower() == 'q': break
        if name and name not in players:
            players.append(name)
            save_data(data)
        else:
            print("Invalid or duplicate name.")

    if len(players) == 8:
        print("\n🎉 Roster Complete!")
        if input("Shuffle seeds? (y/n): ").lower() == 'y':
            random.shuffle(players)
        
        # Setup Quarterfinals
        m = data['matches']
        m['qf1']['p1'], m['qf1']['p2'] = players[0], players[1]
        m['qf2']['p1'], m['qf2']['p2'] = players[2], players[3]
        m['qf3']['p1'], m['qf3']['p2'] = players[4], players[5]
        m['qf4']['p1'], m['qf4']['p2'] = players[6], players[7]
        save_data(data)
        print("⚔️ Matches generated!")
    input("Press Enter...")

def play_match(data, match_id, title, next_match=None, next_slot=None):
    match = data['matches'][match_id]
    if not match['p1'] or not match['p2']:
        print(f"\n⚠️ {title} is not ready yet.")
    elif match['winner']:
        print(f"\n✅ {title} finished. Winner: {match['winner']}")
    else:
        print(f"\n--- {title} ---")
        print(f"1) {match['p1']}\n2) {match['p2']}")
        win = input("Winner (1 or 2): ")
        if win in ['1', '2']:
            winner = match['p1'] if win == '1' else match['p2']
            match['winner'] = winner
            if next_match: data['matches'][next_match][next_slot] = winner
            save_data(data)
            print(f"🏆 {winner} advances!")
    input("Press Enter...")

def main():
    while True:
        clear_screen()
        data = load_data()
        print("🏆 ULTIMATE PLAYER S12: COMMAND CENTER")
        print(f"Status: {len(data['players'])}/8 Players")
        print("---------------------------------------")
        print("1. Register Players / Generate Fixtures")
        print("2. [L] Result: Quarterfinal 1")
        print("3. [L] Result: Quarterfinal 2")
        print("4. [R] Result: Quarterfinal 3")
        print("5. [R] Result: Quarterfinal 4")
        print("6. [L] Result: Semifinal 1")
        print("7. [R] Result: Semifinal 2")
        print("8. [!] GRAND FINAL")
        print("R. Reset All")
        print("Q. Quit")
        
        choice = input("\nAction: ").lower()
        if choice == '1': register_players(data)
        elif choice == '2': play_match(data, 'qf1', 'QF1', 'sf1', 'p1')
        elif choice == '3': play_match(data, 'qf2', 'QF2', 'sf1', 'p2')
        elif choice == '4': play_match(data, 'qf3', 'QF3', 'sf2', 'p1')
        elif choice == '5': play_match(data, 'qf4', 'QF4', 'sf2', 'p2')
        elif choice == '6': play_match(data, 'sf1', 'SF1', 'final', 'p1')
        elif choice == '7': play_match(data, 'sf2', 'SF2', 'final', 'p2')
        elif choice == '8': play_match(data, 'final', 'FINAL')
        elif choice == 'r':
            if input("Wipe everything? (y/n): ") == 'y': save_data(DEFAULT_STATE)
        elif choice == 'q': break

if __name__ == "__main__":
    main()