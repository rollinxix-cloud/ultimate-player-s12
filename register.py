import json
import os
import random

JSON_FILE = 'players.json'

def load_players():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_players(players):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=4)

def main():
    print("=========================================")
    print(" 🏆 ULTIMATE PLAYER SEASON 12 REGISTRATION ")
    print("=========================================\n")
    
    players = load_players()
    
    print(f"Current Registration Status: {len(players)} / 8 Players")
    for i, player in enumerate(players):
        print(f"  [{i+1}] {player}")
    print("-" * 41)

    if len(players) >= 8:
        print("\n⚠️ Roster is currently FULL!")
        choice = input("Would you like to clear the roster and start over? (y/n): ").strip().lower()
        if choice == 'y':
            players = []
            save_players(players)
            print("✨ Roster cleared successfully.")
        else:
            print("Exiting registration system.")
            return

    while len(players) < 8:
        remaining = 8 - len(players)
        print(f"\nNeed {remaining} more player(s) to complete the bracket.")
        name = input(f"Enter name for Player #{len(players) + 1} (or type 'q' to quit): ").strip()
        
        if name.lower() == 'q':
            print("Saving progress and exiting...")
            break
        if not name:
            print("❌ Error: Player name cannot be blank.")
            continue
        if name in players:
            print("❌ Error: This player name is already registered.")
            continue
            
        players.append(name)
        save_players(players)
        print(f"✅ Successfully registered: {name}")

    if len(players) == 8:
        print("\n🎉 All 8 player positions filled!")
        shuffle_choice = input("Would you like to randomly shuffle the bracket seedings? (y/n): ").strip().lower()
        if shuffle_choice == 'y':
            random.shuffle(players)
            save_players(players)
            print("🎲 Tournament seeds randomized successfully!")
        
        print("\n🚀 Ready for deployment! Push your changes to GitHub to update the live bracket.")

if __name__ == '__main__':
    main()