import random
import time
import os

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.attack = 15
        self.defense = 5
        self.skills = ["Antivirus Basic"]
        self.inventory = []
        self.healed_students = 0
        self.healed_teachers = 0
        self.position = "Gerbang Sekolah"
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        
    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.exp_to_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_level = int(self.exp_to_level * 1.5)
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 3
        print(f"\n🎉 LEVEL UP! Kamu sekarang level {self.level}!")
        print(f"HP Max: {self.max_hp} | ATK: {self.attack} | DEF: {self.defense}")
        time.sleep(2)

class Enemy:
    def __init__(self, name, level, hp, attack, defense, exp_reward, enemy_type):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.enemy_type = enemy_type
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage

class Game:
    def __init__(self):
        self.player = None
        self.rooms = {
            "Gerbang Sekolah": {
                "desc": "Kamu berada di gerbang sekolah. Suasana mencekam, layar komputer berkedip-kedip merah.",
                "connections": ["Halaman", "Ruang Tata Usaha"],
                "items": ["Health Potion"],
                "enemy": None
            },
            "Halaman": {
                "desc": "Halaman sekolah yang luas. Beberapa siswa berkeliaran dengan mata menyala merah.",
                "connections": ["Gerbang Sekolah", "Kelas 10A", "Lapangan"],
                "items": [],
                "enemy": "student"
            },
            "Kelas 10A": {
                "desc": "Kelas 10A. Ada 3 siswa yang terinfeksi malware di sini.",
                "connections": ["Halaman", "Kelas 10B", "Koridor Lantai 1"],
                "items": ["Firewall Shield"],
                "enemy": "student"
            },
            "Kelas 10B": {
                "desc": "Kelas 10B. Papan tulis menampilkan kode-kode aneh.",
                "connections": ["Kelas 10A", "Koridor Lantai 1"],
                "items": [],
                "enemy": "student"
            },
            "Koridor Lantai 1": {
                "desc": "Koridor lantai 1. Lampu berkedip-kedip.",
                "connections": ["Kelas 10A", "Kelas 10B", "Tangga", "Lab Komputer"],
                "items": ["Health Potion"],
                "enemy": None
            },
            "Lab Komputer": {
                "desc": "Lab Komputer. Semua komputer terinfeksi! Ada guru TI yang terinfeksi di sini.",
                "connections": ["Koridor Lantai 1"],
                "items": ["Encryption Key"],
                "enemy": "teacher"
            },
            "Tangga": {
                "desc": "Tangga menuju lantai 2.",
                "connections": ["Koridor Lantai 1", "Koridor Lantai 2"],
                "items": [],
                "enemy": None
            },
            "Koridor Lantai 2": {
                "desc": "Koridor lantai 2. Lebih gelap dari lantai 1.",
                "connections": ["Tangga", "Ruang Guru", "Perpustakaan"],
                "items": ["Health Potion"],
                "enemy": None
            },
            "Ruang Guru": {
                "desc": "Ruang Guru. Beberapa guru terinfeksi malware tingkat menengah!",
                "connections": ["Koridor Lantai 2"],
                "items": ["Malware Scanner"],
                "enemy": "teacher"
            },
            "Perpustakaan": {
                "desc": "Perpustakaan. Buku-buku bertuliskan kode binary.",
                "connections": ["Koridor Lantai 2", "Ruang Kepala Sekolah"],
                "items": ["System Restore"],
                "enemy": "teacher"
            },
            "Ruang Kepala Sekolah": {
                "desc": "⚠️ RUANG KEPALA SEKOLAH ⚠️\nAura malware tingkat tinggi terasa sangat kuat!",
                "connections": ["Perpustakaan"],
                "items": ["Ultimate Antivirus"],
                "enemy": "principal"
            },
            "Ruang Tata Usaha": {
                "desc": "Ruang Tata Usaha. Ada beberapa staf yang terinfeksi.",
                "connections": ["Gerbang Sekolah", "Lapangan"],
                "items": [],
                "enemy": "teacher"
            },
            "Lapangan": {
                "desc": "Lapangan olahraga. Siswa-siswa terinfeksi sedang berlarian.",
                "connections": ["Halaman", "Ruang Tata Usaha"],
                "items": ["Health Potion"],
                "enemy": "student"
            }
        }
        self.cleared_rooms = []
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_status(self):
        print("\n" + "="*60)
        print(f"👤 {self.player.name} | Level {self.player.level} | HP: {self.player.hp}/{self.player.max_hp} | EXP: {self.player.exp}/{self.player.exp_to_level}")
        print(f"⚔️ ATK: {self.player.attack} | 🛡️ DEF: {self.player.defense}")
        print(f"📍 Lokasi: {self.player.position}")
        print(f"👥 Disembuhkan: Siswa {self.player.healed_students} | Guru {self.player.healed_teachers}")
        print("="*60 + "\n")
    
    def create_enemy(self, enemy_type):
        if enemy_type == "student":
            names = ["Siswa Terinfeksi", "Murid yang Terkena Malware", "Pelajar Bermalware"]
            return Enemy(random.choice(names), random.randint(1, 3), 
                        random.randint(30, 50), random.randint(8, 12), 
                        random.randint(2, 4), 30, "student")
        elif enemy_type == "teacher":
            names = ["Guru Terinfeksi", "Pengajar Bermalware", "Staff Terkena Virus"]
            return Enemy(random.choice(names), random.randint(4, 6),
                        random.randint(60, 90), random.randint(15, 20),
                        random.randint(5, 8), 60, "teacher")
        elif enemy_type == "principal":
            return Enemy("🔴 KEPALA SEKOLAH - MALWARE TINGKAT TINGGI 🔴", 10,
                        200, 30, 15, 200, "principal")
    
    def battle(self, enemy):
        print(f"\n⚔️ PERTARUNGAN DIMULAI! ⚔️")
        print(f"Kamu berhadapan dengan {enemy.name}!")
        print(f"Level: {enemy.level} | HP: {enemy.hp}/{enemy.max_hp}")
        time.sleep(1)
        
        while self.player.hp > 0 and enemy.hp > 0:
            print("\n" + "-"*60)
            print(f"💚 HP Kamu: {self.player.hp}/{self.player.max_hp} | 🔴 HP {enemy.name}: {enemy.hp}/{enemy.max_hp}")
            print("\nPilih Aksi:")
            print("1. 🗡️ Serang Normal")
            print("2. 🔧 Gunakan Skill")
            print("3. 🎒 Gunakan Item")
            print("4. 🏃 Kabur")
            
            choice = input("\nPilihan: ").strip()
            
            if choice == "1":
                # Player attack
                damage = random.randint(self.player.attack - 3, self.player.attack + 5)
                actual_damage = enemy.take_damage(damage)
                print(f"\n💥 Kamu menyerang dengan Antivirus! Damage: {actual_damage}")
                time.sleep(1)
                
                if enemy.hp <= 0:
                    break
                
                # Enemy attack
                enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                player_damage = self.player.take_damage(enemy_damage)
                print(f"⚡ {enemy.name} menyerang dengan Malware! Damage: {player_damage}")
                time.sleep(1)
                
            elif choice == "2":
                self.use_skill(enemy)
                # Enemy attack
                if enemy.hp > 0:
                    enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                    player_damage = self.player.take_damage(enemy_damage)
                    print(f"⚡ {enemy.name} menyerang dengan Malware! Damage: {player_damage}")
                    time.sleep(1)
                    
            elif choice == "3":
                if not self.use_item():
                    continue
                # Enemy attack
                enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                player_damage = self.player.take_damage(enemy_damage)
                print(f"⚡ {enemy.name} menyerang dengan Malware! Damage: {player_damage}")
                time.sleep(1)
                
            elif choice == "4":
                if random.random() < 0.5:
                    print("\n🏃 Kamu berhasil kabur!")
                    time.sleep(1)
                    return False
                else:
                    print("\n❌ Gagal kabur!")
                    enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                    player_damage = self.player.take_damage(enemy_damage)
                    print(f"⚡ {enemy.name} menyerang! Damage: {player_damage}")
                    time.sleep(1)
        
        if self.player.hp <= 0:
            print("\n💀 GAME OVER! Kamu terinfeksi malware...")
            return False
        
        if enemy.hp <= 0:
            print(f"\n✅ {enemy.name} berhasil disembuhkan!")
            print(f"💎 Kamu mendapat {enemy.exp_reward} EXP!")
            self.player.gain_exp(enemy.exp_reward)
            
            # Update counter
            if enemy.enemy_type == "student":
                self.player.healed_students += 1
            elif enemy.enemy_type == "teacher":
                self.player.healed_teachers += 1
            
            # Learn new skill
            self.learn_skill(enemy.enemy_type)
            time.sleep(2)
            return True
    
    def use_skill(self, enemy):
        print("\n🔧 Skill yang tersedia:")
        for i, skill in enumerate(self.player.skills, 1):
            print(f"{i}. {skill}")
        print(f"{len(self.player.skills)+1}. Kembali")
        
        choice = input("\nPilih skill: ").strip()
        
        try:
            skill_idx = int(choice) - 1
            if 0 <= skill_idx < len(self.player.skills):
                skill = self.player.skills[skill_idx]
                
                if skill == "Antivirus Basic":
                    damage = int(self.player.attack * 1.5)
                    actual_damage = enemy.take_damage(damage)
                    print(f"\n🔥 {skill}! Damage: {actual_damage}")
                elif skill == "Firewall Blast":
                    damage = int(self.player.attack * 2)
                    actual_damage = enemy.take_damage(damage)
                    print(f"\n🔥 {skill}! Damage: {actual_damage}")
                    self.player.defense += 2
                    print(f"🛡️ Defense meningkat +2!")
                elif skill == "System Scan":
                    damage = int(self.player.attack * 2.5)
                    actual_damage = enemy.take_damage(damage)
                    print(f"\n🔥 {skill}! Damage: {actual_damage}")
                    heal = 15
                    self.player.heal(heal)
                    print(f"💚 HP pulih +{heal}!")
                elif skill == "Full System Restore":
                    damage = int(self.player.attack * 3)
                    actual_damage = enemy.take_damage(damage)
                    print(f"\n🔥 {skill}! MASSIVE DAMAGE: {actual_damage}")
                    
                time.sleep(1)
        except:
            return
    
    def use_item(self):
        if not self.player.inventory:
            print("\n❌ Inventory kosong!")
            time.sleep(1)
            return False
            
        print("\n🎒 Inventory:")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item}")
        print(f"{len(self.player.inventory)+1}. Kembali")
        
        choice = input("\nPilih item: ").strip()
        
        try:
            item_idx = int(choice) - 1
            if 0 <= item_idx < len(self.player.inventory):
                item = self.player.inventory[item_idx]
                
                if "Health Potion" in item:
                    heal = 40
                    self.player.heal(heal)
                    print(f"\n💚 Menggunakan {item}! HP +{heal}")
                    self.player.inventory.pop(item_idx)
                    time.sleep(1)
                    return True
                elif "Shield" in item:
                    self.player.defense += 5
                    print(f"\n🛡️ Menggunakan {item}! Defense +5")
                    self.player.inventory.pop(item_idx)
                    time.sleep(1)
                    return True
                else:
                    print(f"\n📦 {item} disimpan untuk nanti")
                    time.sleep(1)
                    return False
        except:
            return False
    
    def learn_skill(self, enemy_type):
        new_skill = None
        
        if enemy_type == "student" and self.player.healed_students == 1:
            new_skill = "Firewall Blast"
        elif enemy_type == "teacher" and self.player.healed_teachers == 1:
            new_skill = "System Scan"
        elif enemy_type == "teacher" and self.player.healed_teachers == 2:
            new_skill = "Full System Restore"
        
        if new_skill and new_skill not in self.player.skills:
            self.player.skills.append(new_skill)
            print(f"\n🎓 SKILL BARU DIPELAJARI: {new_skill}!")
            time.sleep(2)
    
    def explore_room(self):
        room = self.rooms[self.player.position]
        
        self.clear_screen()
        self.show_status()
        print(room["desc"])
        
        # Check for items
        if room["items"] and self.player.position not in self.cleared_rooms:
            print(f"\n📦 Item ditemukan: {', '.join(room['items'])}")
            for item in room["items"]:
                self.player.inventory.append(item)
            print(f"✅ Item ditambahkan ke inventory!")
            time.sleep(1)
        
        # Check for enemy
        if room["enemy"] and self.player.position not in self.cleared_rooms:
            time.sleep(1)
            enemy = self.create_enemy(room["enemy"])
            
            # Special message for principal
            if enemy.enemy_type == "principal":
                print("\n" + "="*60)
                print("⚠️  BOSS FIGHT - KEPALA SEKOLAH TERINFEKSI MALWARE TINGKAT TINGGI ⚠️")
                print("Ini adalah pertarungan terakhir! Bersiaplah!")
                print("="*60)
                time.sleep(2)
            
            result = self.battle(enemy)
            
            if not result:
                return False
            
            # Mark room as cleared
            self.cleared_rooms.append(self.player.position)
            
            # Check if principal is defeated
            if enemy.enemy_type == "principal":
                self.game_won()
                return False
        
        # Show connections
        print(f"\n🚪 Pintu yang tersedia:")
        for i, connection in enumerate(room["connections"], 1):
            print(f"{i}. {connection}")
        print(f"{len(room['connections'])+1}. Lihat Status")
        print(f"{len(room['connections'])+2}. Lihat Inventory")
        
        return True
    
    def game_won(self):
        self.clear_screen()
        print("\n" + "="*60)
        print("🎉🎉🎉 SELAMAT! KAMU MENANG! 🎉🎉🎉")
        print("="*60)
        print(f"\n{self.player.name} berhasil menyembuhkan Kepala Sekolah!")
        print("Semua malware telah dibersihkan dari sekolah!")
        print(f"\nStatistik Akhir:")
        print(f"Level: {self.player.level}")
        print(f"Siswa Disembuhkan: {self.player.healed_students}")
        print(f"Guru/Staff Disembuhkan: {self.player.healed_teachers}")
        print("\nTerima kasih telah bermain!")
        print("="*60)
        time.sleep(3)
    
    def play(self):
        self.clear_screen()
        print("="*60)
        print("        🏫 MALWARE SCHOOL RPG 🏫")
        print("="*60)
        print("\nSelamat datang di SMKN 1 BRONDONG!")
        print("Namun... terjadi bencana! Seluruh warga sekolah terinfeksi malware!")
        print("\nKamu adalah satu-satunya yang tidak terinfeksi.")
        print("Tugas kamu: Sembuhkan semua orang dengan kekuatan Antivirus!")
        print("\nTingkat Infeksi:")
        print("- Siswa: Malware Ringan")
        print("- Guru/Staff: Malware Menengah")
        print("- Kepala Sekolah: Malware Tingkat Tinggi (BOSS)")
        print("\n" + "="*60)
        
        name = input("\nMasukkan nama kamu: ").strip()
        if not name:
            name = "Hacker"
        
        self.player = Player(name)
        
        print(f"\nSelamat datang, {name}!")
        print("Petualanganmu dimulai...")
        time.sleep(2)
        
        # Game loop
        while self.player.hp > 0:
            if not self.explore_room():
                break
            
            room = self.rooms[self.player.position]
            choice = input("\nPilih tujuan: ").strip()
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(room["connections"]):
                    self.player.position = room["connections"][choice_num - 1]
                elif choice_num == len(room["connections"]) + 1:
                    self.clear_screen()
                    self.show_status()
                    print("Skills:", ", ".join(self.player.skills))
                    input("\nTekan Enter untuk lanjut...")
                elif choice_num == len(room["connections"]) + 2:
                    self.clear_screen()
                    print("\n🎒 INVENTORY:")
                    if self.player.inventory:
                        for item in self.player.inventory:
                            print(f"  - {item}")
                    else:
                        print("  (Kosong)")
                    input("\nTekan Enter untuk lanjut...")
            except:
                print("Pilihan tidak valid!")
                time.sleep(1)
        
        if self.player.hp <= 0:
            print("\n💀 GAME OVER!")
            print("Kamu terinfeksi malware dan tidak bisa melanjutkan...")

# Run game
if __name__ == "__main__":
    game = Game()
    game.play()

