import random
import time
import csv
from prettytable import PrettyTable
import pwinput 

data_file = "data_pa.csv"
menu_file = "menu.csv"

user_admin = "admin"
pw_admin = "admin123"

nama_driver = ["Agus", "Budiono", "Siregar", "Dewi", "Eko", "Fajar", "Gina", "Hana"]

def init_files():
    # Inisialisasi file menu.csv jika belum ada
    try:
        with open(menu_file, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["nama_menu", "harga"])
    except FileExistsError:
        pass

    # Inisialisasi file data_pa.csv jika belum ada
    try:
        with open(data_file, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "role", "saldo_gopay"])
    except FileExistsError:
        pass
def memuatdata():
    user = {}
    try:
        with open(data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) == 4:
                    username, password, pengguna, saldo_gopay = row
                    user[username] = {"password": password, "role": pengguna, "saldo_gopay": int(saldo_gopay)}
    except FileNotFoundError:
        pass
    return user

def menyimpandata(users):
    with open(data_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role", "saldo_gopay"]) 
        for username, info in users.items(): 
            writer.writerow([username, info["password"], info["role"], info["saldo_gopay"]])

def baca_menu():
    menu = {}
    try:
        with open(menu_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                menu[row['nama_menu']] = int(row['harga'])
    except FileNotFoundError:
        init_files()
        return baca_menu()
    return menu

def simpan_menu(menu):
    with open(menu_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['nama_menu', 'harga'])
        writer.writeheader()
        for nama_menu, harga in menu.items():
            writer.writerow({'nama_menu': nama_menu, 'harga': harga})

def register(users):
    print("\n=================")
    print("|   REGISTER   |")
    print("================")
    username = input("Username: ")
    if username in users:
        print("USERNAME SUDAH DIGUNAKAN!.")
        return None
    password = pwinput.pwinput("Password: ")
    role = "user"
    users[username] = {"password": password, "role": role, "saldo_gopay": 0}
    menyimpandata(users)
    print("REGISTRASI BERHASIL, SILAHKAN LOGIN!")
    return username

def login(users):
    print("\n================")
    print("|    LOGIN     |")
    print("================")
    username = input("Username: ")
    password = pwinput.pwinput("Password: ")
    
    if username == user_admin and password == pw_admin:
        print("\nLOADING......... 20%")
        time.sleep(1)
        print("LOADING........... 40%")
        time.sleep(1)
        print("LOADING........... 80%")
        time.sleep(1)
        print("LOADING...........100%")
        time.sleep(1)
        print("\n====================")
        print("|  BERHASIL LOGIN  |")
        print("|  SEBAGAI ADMIN   |")
        print("====================")
        return username, "admin"
    elif username in users and users[username]["password"] == password:
        print("\nLOADING..........20%")
        time.sleep(1)
        print("LOADING........... 40%")
        time.sleep(1)
        print("LOADING........... 80%")
        time.sleep(1)
        print("LOADING...........100%")
        time.sleep(1)
        print("\n======================")
        print("|   BERHASIL LOGIN   |")
        print("|   SEBAGAI USER     |")
        print("======================")
        time.sleep(1)
        return username, users[username]["role"]
    else:
        print("\n====================")
        print("|   LOGIN GAGAL!   |")
        print("====================")
        return None, None

def tampilkan_menu():
    menu = baca_menu()
    table = PrettyTable()
    table.field_names = ["No", "Menu", "Harga"]
    for idx, (nama_menu, harga) in enumerate(menu.items(), 1):
        table.add_row([idx, nama_menu, f"Rp{harga}"])
    print(table)

def tambah_menu():
    menu = baca_menu()
    nama_menu = input("Masukkan nama menu baru: ")
    if nama_menu in menu:
        print("Menu sudah ada!")
        return
    try:
        harga = int(input("Masukkan harga menu: Rp"))
        menu[nama_menu] = harga
        simpan_menu(menu)
        print(f"Menu {nama_menu} berhasil ditambahkan!")
    except ValueError:
        print("Harga harus berupa angka!")

def hapus_menu():
    menu = baca_menu()
    tampilkan_menu()
    nama_menu = input("\nMasukkan nama menu yang ingin dihapus: ")
    if nama_menu in menu:
        del menu[nama_menu]
        simpan_menu(menu)
        print(f"Menu {nama_menu} berhasil dihapus!")
    else:
        print("Menu tidak ditemukan!")

def ubah_menu():
    menu = baca_menu()
    tampilkan_menu()
    nama_menu = input("\nMasukkan nama menu yang ingin diubah: ")
    if nama_menu in menu:
        try:
            nama_baru = input("Masukkan nama menu baru: ")
            harga_baru = int(input("Masukkan harga baru: Rp"))
            del menu[nama_menu]
            menu[nama_baru] = harga_baru
            simpan_menu(menu)
            print("Menu berhasil diubah!")
        except ValueError:
            print("Harga harus berupa angka!")
    else:
        print("Menu tidak ditemukan!")

def pilih_menu():
    menu = baca_menu()
    print("\nSilakan pilih menu dengan nomor yang sesuai:")
    tampilkan_menu()
    try:
        pilihan = int(input("\nMasukkan nomor menu yang ingin Anda pesan (0 untuk batal): "))
        if pilihan == 0:
            print("Pesanan dibatalkan.")
            return None
        elif 1 <= pilihan <= len(menu):
            nama_menu = list(menu.keys())[pilihan - 1]
            return nama_menu, menu[nama_menu]
        else:
            print("Nomor menu tidak valid!")
            return None
    except ValueError:
        print("Input harus berupa angka!")
        return None

def ambil_harga(menu_item):
    # Fungsi ini akan mengambil elemen harga dari item menu
    return menu_item[1]

def sortir_termurah():
    # Baca menu dari file
    menu = baca_menu()
    
    # Ubah menu menjadi list berisi pasangan [nama_menu, harga]
    daftar_menu = []
    for nama_menu, harga in menu.items():
        daftar_menu.append([nama_menu, harga])
    
    # Urutkan berdasarkan harga dengan menggunakan fungsi `ambil_harga`
    daftar_menu.sort(key=ambil_harga)
    
    # Buat tabel untuk menampilkan hasil
    table = PrettyTable()
    table.field_names = ["No", "Menu", "Harga"]
    
    # Masukkan data ke tabel
    nomor = 1
    for menu in daftar_menu:
        nama_menu = menu[0]
        harga = menu[1]
        table.add_row([nomor, nama_menu, f"Rp{harga}"])
        nomor += 1
    
    # Tampilkan hasil
    print("\nMenu (dari termurah):")
    print(table)


def sortir_termahal():
    menu = baca_menu()
    menu_sorted = dict(sorted(menu.items(), key=lambda x: x[1], reverse=True))
    table = PrettyTable()
    table.field_names = ["No", "Menu", "Harga"]
    for idx, (nama_menu, harga) in enumerate(menu_sorted.items(), 1):
        table.add_row([idx, nama_menu, f"Rp{harga}"])
    print("\nMenu (dari termahal):")
    print(table)

def admin_menu(users):
    while True:
        table = PrettyTable()
        table.field_names = ["Menu Admin"]
        table.add_rows([
            ["1. Tampilkan Menu"],
            ["2. Tambah Menu"],
            ["3. Hapus Menu"],
            ["4. Ubah Menu"],
            ["5. Kelola Data User"],
            ["6. Keluar"]
        ])
        print(table)
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_menu()
        elif pilihan == "2":
            tambah_menu()
        elif pilihan == "3":
            hapus_menu()
        elif pilihan == "4":
            ubah_menu()
        elif pilihan == "5":
            kelola_user(users)
        elif pilihan == "6":
            break
        else:
            print("Pilihan tidak valid!")

def kelola_user(users):
    while True:
        table = PrettyTable()
        table.field_names = ["Menu Kelola User"]
        table.add_rows([
            ["1. Tampilkan Data User"],
            ["2. Ubah Username"],
            ["3. Ubah Saldo"],
            ["4. Kembali"]
        ])
        print(table)
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_data_user(users)
        elif pilihan == "2":
            ubah_username(users)
        elif pilihan == "3":
            ubah_saldo(users)
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid!")

def tampilkan_data_user(users):
    table = PrettyTable()
    table.field_names = ["Username", "Role", "Saldo"]
    for username, info in users.items():
        if info["role"] != "admin":  
            table.add_row([username, info["role"], f"Rp{info['saldo_gopay']}"])
    print(table)

def ubah_username(users):
    tampilkan_data_user(users)
    username_lama = input("\nMasukkan username yang ingin diubah: ")
    if username_lama in users and users[username_lama]["role"] != "admin":
        username_baru = input("Masukkan username baru: ")
        if username_baru not in users:
            users[username_baru] = users.pop(username_lama)
            menyimpandata(users)
            print("Username berhasil diubah!")
        else:
            print("Username baru sudah digunakan!")
    else:
        print("Username tidak ditemukan!")

def ubah_saldo(users):
    tampilkan_data_user(users)
    username = input("\nMasukkan username yang ingin diubah saldonya: ")
    if username in users and users[username]["role"] != "admin":
        try:
            saldo_baru = int(input("Masukkan saldo baru: Rp"))
            users[username]["saldo_gopay"] = saldo_baru
            menyimpandata(users)
            print("Saldo berhasil diubah!")
        except ValueError:
            print("Saldo harus berupa angka!")
    else:
        print("Username tidak ditemukan!")

def proses_pesanan(users, username):
    pesanan = []
    total_harga = 0

    while True:
        print("\n=== Menu Pemesanan ===")
        print("1. Tampilkan Menu (Termurah)")
        print("2. Tampilkan Menu (Termahal)")
        print("3. Pesan")
        print("4. Kembali")
        
        pilihan = input("\nPilih menu (1-4): ")
        
        if pilihan == "1":
            sortir_termurah()
        elif pilihan == "2":
            sortir_termahal()
        elif pilihan == "3":
            hasil = pilih_menu()
            if hasil:
                nama_menu, harga = hasil
                try:
                    jumlah = int(input("Masukkan jumlah pesanan: "))
                    if jumlah <= 0:
                        print("Jumlah pesanan harus lebih dari 0!")
                        continue
                    
                    subtotal = harga * jumlah
                    total_harga += subtotal
                    pesanan.append({
                        "item": nama_menu,
                        "jumlah": jumlah,
                        "total": subtotal
                    })
                    
                    if input("Pesan menu lain? (y/t): ").lower() != 'y':
                        if proses_pembayaran(users, username, total_harga):
                            driver = random.choice(nama_driver)
                            waktu = estimasi_waktu()
                            print(f"\nMencari driver... \nDriver {driver} akan mengantarkan pesanan dalam {waktu} menit.")
                            time.sleep(2)
                            print("Driver sedang mengantar pesanan Anda...")
                            time.sleep(2)
                            print("Pesanan telah sampai!")
                            buat_invoice(username, pesanan, users[username]["saldo_gopay"])
                            return pesanan
                except ValueError:
                    print("Jumlah pesanan harus berupa angka!")
        elif pilihan == "4":
            return None
        else:
            print("Pilihan tidak valid!")

def estimasi_waktu():
    return random.randint(5, 20)

def buat_invoice(username, pesanan, saldo_akhir):
    print("\n=======================================")
    print(" |         INVOICE PEMBAYARAN           |")
    print("==========================================")
    table = PrettyTable()
    table.field_names = ["Menu", "Jumlah", "Total"]
    total = 0
    
    for item in pesanan:
        table.add_row([
            item["item"],
            item["jumlah"],
            f"Rp{item['total']}"
        ])
        total += item["total"]
        
    print(table)
    print(f"Total Pembayaran: Rp{total}")
    print(f"Saldo GoPay Tersisa: Rp{saldo_akhir}")
    print("Terima kasih telah menggunakan GoFood!")

def proses_pembayaran(users, username, total_harga):
    if users[username]["saldo_gopay"] >= total_harga:
        users[username]["saldo_gopay"] -= total_harga
        menyimpandata(users)
        print(f"\nPembayaran berhasil! Sisa saldo: Rp{users[username]['saldo_gopay']}")
        return True
    else:
        print(f"\nSaldo tidak cukup! Saldo Anda: Rp{users[username]['saldo_gopay']}")
        return False

def cek_saldo(users, username):
    table = PrettyTable()
    table.field_names = ["Username", "Saldo GoPay"]
    table.add_row([username, f"Rp{users[username]['saldo_gopay']}"])
    print(table)

def tambah_saldo(users, username):
    try:
        tambahan = int(input("Masukkan jumlah saldo yang ingin ditambahkan: Rp"))
        if tambahan > 0:
            users[username]["saldo_gopay"] += tambahan
            menyimpandata(users)
            print(f"Saldo berhasil ditambahkan! Saldo saat ini: Rp{users[username]['saldo_gopay']}")
        else:
            print("Jumlah saldo harus lebih dari 0!")
    except ValueError:
        print("Input harus berupa angka!")

def user_menu(users, username):
    while True:
        table = PrettyTable()
        table.field_names = ["Menu User"]
        table.add_rows([
            ["1. Pesan Makanan"],
            ["2. Cek Saldo"],
            ["3. Tambah Saldo"],
            ["4. Keluar"]
        ])
        print(table)
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            proses_pesanan(users, username)
        elif pilihan == "2":
            cek_saldo(users, username)
        elif pilihan == "3":
            tambah_saldo(users, username)
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid!")

def main():
    init_files()
    users = memuatdata()
    
    while True:
        table = PrettyTable()
        table.field_names = ["Selamat Datang di GoFood"]
        table.add_rows([
            ["1. Login"],
            ["2. Register"],
            ["3. Keluar"]
        ])
        print(table)
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            username, role = login(users)
            if username and role == "admin":
                admin_menu(users)
            elif username and role == "user":
                user_menu(users, username)
        elif pilihan == "2":
            username = register(users)
            if username:
                user_menu(users, username)
        elif pilihan == "3":
            print("Terima kasih telah menggunakan GoFood!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
