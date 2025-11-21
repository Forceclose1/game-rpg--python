import random
import time

class Character:
    def __init__(self, name, hp, attack, defense, character_type):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.character_type = character_type
        self.inventory = []
        self.level = 1
        self.exp = 0
    
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)  # Minimal 1 damage
        self.hp -= actual_damage
        if self.hp < 0:
            self.hp = 0
        return actual_damage
    
    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed = self.hp - old_hp
        return healed
    
    def attack_enemy(self, enemy):
        base_damage = self.attack
        damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        
        is_crit = random.random() < 0.2
        if is_crit:
            damage = int(damage * 1.5)
        
        actual_damage = enemy.take_damage(damage)
        return actual_damage, is_crit
    
    def add_item(self, item):
        self.inventory.append(item)
    
    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory.pop(item_index)
            return item
        return None
    
    def gain_exp(self, amount):
        self.exp += amount
        exp_needed = self.level * 50
        
        if self.exp >= exp_needed:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        self.level += 1
        self.exp = 0
        
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
    
    def show_stats(self):
        print(f"\n{'='*50}")
        print(f"  {self.name} ({self.character_type}) - Level {self.level}")
        print(f"{'='*50}")
        print(f"  HP      : {self.hp}/{self.max_hp}")
        print(f"  Attack  : {self.attack}")
        print(f"  Defense : {self.defense}")
        print(f"  EXP     : {self.exp}/{self.level * 50}")
        print(f"  Inventory: {len(self.inventory)} items")
        print(f"{'='*50}\n")

def create_player():
    print("\n" + "="*60)
    print("  SELAMAT DATANG DI DUNGEON WARRIOR  ".center(60))
    print("="*60 + "\n")
    
    name = input("Masukkan nama karakter Anda: ").strip()
    if not name:
        name = "Hero"
    
    print(f"\nHalo, {name}! Pilih kelas karakter Anda:\n")
    print("1. WARRIOR  - HP: 150 | Attack: 25 | Defense: 15")
    print("              (Tanker dengan defense tinggi)")
    print("\n2. MAGE     - HP: 100 | Attack: 35 | Defense: 8")
    print("              (Damage tinggi tapi rapuh)")
    print("\n3. ROGUE    - HP: 120 | Attack: 30 | Defense: 10")
    print("              (Seimbang antara attack dan defense)")
    
    while True:
        choice = input("\nPilih kelas (1/2/3): ").strip()
        if choice == '1':
            player = Character(name, 150, 25, 15, "Warrior")
            break
        elif choice == '2':
            player = Character(name, 100, 35, 8, "Mage")
            break
        elif choice == '3':
            player = Character(name, 120, 30, 10, "Rogue")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1, 2, atau 3.")
    
    
    player.add_item({"name": "Health Potion", "type": "heal", "value": 40})
    player.add_item({"name": "Health Potion", "type": "heal", "value": 40})
    
    print(f"\n✓ Karakter {player.name} ({player.character_type}) berhasil dibuat!")
    print("✓ Anda mendapat 2x Health Potion sebagai starting item!")
    time.sleep(2)
    
    return player

def create_enemy(player_level):
    enemies = [
        {"name": "Goblin", "hp": 60, "attack": 15, "defense": 5},
        {"name": "Orc", "hp": 80, "attack": 20, "defense": 8},
        {"name": "Dark Knight", "hp": 100, "attack": 25, "defense": 12},
        {"name": "Dragon Whelp", "hp": 120, "attack": 30, "defense": 10},
        {"name": "Ancient Demon", "hp": 150, "attack": 35, "defense": 15},
    ]
    
    enemy_index = min(player_level - 1, len(enemies) - 1)
    enemy_data = enemies[enemy_index].copy()
    
    level_multiplier = 1 + (player_level - 1) * 0.2
    enemy_data["hp"] = int(enemy_data["hp"] * level_multiplier)
    enemy_data["attack"] = int(enemy_data["attack"] * level_multiplier)
    enemy_data["defense"] = int(enemy_data["defense"] * level_multiplier)
    
    enemy = Character(
        enemy_data["name"],
        enemy_data["hp"],
        enemy_data["attack"],
        enemy_data["defense"],
        "Enemy"
    )
    
    return enemy

def show_battle_status(player, enemy):
    print("\n" + "─"*60)
    print(f"  {player.name} (Lv.{player.level})".ljust(30) + f"VS".center(10) + f"{enemy.name}".rjust(20))
    print(f"  HP: {player.hp}/{player.max_hp}".ljust(30) + " "*10 + f"HP: {enemy.hp}/{enemy.max_hp}".rjust(20))
    print("─"*60 + "\n")

def player_turn(player, enemy):
    print("Giliran Anda! Pilih aksi:")
    print("1. ⚔️  Attack")
    print("2. 🛡️  Defend (kurangi damage 50% di giliran musuh)")
    print("3. 🎒 Use Item")
    print("4. 📊 Check Stats")
    
    defending = False
    
    while True:
        choice = input("\nPilih aksi (1/2/3/4): ").strip()
        
        if choice == '1':  # Attack
            damage, is_crit = player.attack_enemy(enemy)
            if is_crit:
                print(f"\n💥 CRITICAL HIT! {player.name} menyerang {enemy.name} sebesar {damage} damage!")
            else:
                print(f"\n⚔️  {player.name} menyerang {enemy.name} sebesar {damage} damage!")
            
            if not enemy.is_alive():
                print(f"💀 {enemy.name} telah dikalahkan!")
            break
        
        elif choice == '2':  # Defend
            defending = True
            print(f"\n🛡️  {player.name} bersiap bertahan! Defense meningkat untuk giliran ini.")
            break
        
        elif choice == '3':  # Use Item
            if not player.inventory:
                print("\n❌ Inventory kosong! Tidak ada item yang bisa digunakan.")
                continue
            
            print("\n🎒 Inventory:")
            for i, item in enumerate(player.inventory):
                print(f"  {i+1}. {item['name']} (Heal: {item['value']} HP)")
            print(f"  0. Kembali")
            
            item_choice = input("\nPilih item (nomor): ").strip()
            
            if item_choice == '0':
                continue
            
            try:
                item_index = int(item_choice) - 1
                item = player.use_item(item_index)
                
                if item and item['type'] == 'heal':
                    healed = player.heal(item['value'])
                    print(f"\n✨ Menggunakan {item['name']}! Restore {healed} HP.")
                    print(f"   HP sekarang: {player.hp}/{player.max_hp}")
                    break
                else:
                    print("\n❌ Item tidak valid!")
            except (ValueError, IndexError):
                print("\n❌ Pilihan tidak valid!")
        
        elif choice == '4':  # Check Stats
            player.show_stats()
            enemy.show_stats()
        
        else:
            print("❌ Pilihan tidak valid! Pilih 1, 2, 3, atau 4.")
    
    return defending

def enemy_turn(player, enemy, player_defending):
    time.sleep(1)
    
    damage, is_crit = enemy.attack_enemy(player)
    
    if player_defending:
        damage = int(damage * 0.5)
        print(f"\n🛡️  {enemy.name} menyerang! {player.name} berhasil bertahan!")
    
    if is_crit and not player_defending:
        print(f"\n💥 CRITICAL HIT! {enemy.name} menyerang {player.name} sebesar {damage} damage!")
    else:
        print(f"\n⚔️  {enemy.name} menyerang {player.name} sebesar {damage} damage!")
    
    if not player.is_alive():
        print(f"💀 {player.name} telah kalah dalam pertempuran...")

def battle(player, enemy):
    print("\n" + "!"*60)
    print(f"  ⚔️  PERTEMPURAN DIMULAI! {enemy.name} muncul!  ⚔️  ".center(60))
    print("!"*60)
    time.sleep(1.5)
    
    turn = 1
    
    while player.is_alive() and enemy.is_alive():
        print(f"\n{'='*60}")
        print(f"  TURN {turn}  ".center(60))
        print(f"{'='*60}")
        
        show_battle_status(player, enemy)
        
        player_defending = player_turn(player, enemy)
        
        if not enemy.is_alive():
            break
        
        enemy_turn(player, enemy, player_defending)
        
        turn += 1
        time.sleep(1)
    
    time.sleep(1)
    print("\n" + "="*60)
    
    if player.is_alive():
        exp_gained = enemy.max_hp // 2
        gold_gained = random.randint(20, 50)
        
        print("  🎉 KEMENANGAN! 🎉  ".center(60))
        print("="*60)
        print(f"\n✓ Anda mendapat {exp_gained} EXP!")
        print(f"✓ Anda mendapat {gold_gained} Gold!")
        
        
        if random.random() < 0.4:  # 40% chance
            item = {"name": "Health Potion", "type": "heal", "value": 40}
            player.add_item(item)
            print(f"✓ Anda mendapat {item['name']}!")
        
        leveled_up = player.gain_exp(exp_gained)
        if leveled_up:
            print(f"\n🌟 LEVEL UP! {player.name} naik ke Level {player.level}!")
            print(f"   Stats meningkat: HP +20, Attack +5, Defense +3")
        
        return True
    else:
        print("  ☠️  GAME OVER  ☠️  ".center(60))
        print("="*60)
        print(f"\n{player.name} telah gugur dalam pertempuran...")
        return False

def main():
    player = create_player()
    player.show_stats()
    
    battles_won = 0
    
    while player.is_alive():
        input("\nTekan ENTER untuk melanjutkan ke pertempuran berikutnya...")
        
        enemy = create_enemy(player.level)
        result = battle(player, enemy)
        
        if result:
            battles_won += 1
            
            # Restore sedikit HP setelah menang
            restored = player.heal(30)
            if restored > 0:
                print(f"\n💚 Istirahat sejenak... HP restored +{restored}")
            
            time.sleep(2)
        else:
            break
    
    print("\n" + "="*60)
    print("  STATISTIK AKHIR  ".center(60))
    print("="*60)
    print(f"\nNama      : {player.name}")
    print(f"Kelas     : {player.character_type}")
    print(f"Level     : {player.level}")
    print(f"Pertempuran Dimenangkan: {battles_won}")
    print("\nTerima kasih telah bermain DUNGEON WARRIOR!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
