import random
import time
import csv
from prettytable import PrettyTable

data_file = "data_pa.csv"

user_admin = "admin"
pw_admin = "admin123"

menu = {
    "Nasi Goreng": 30000,
    "Ayam Geprek": 25000,
    "Bakso"      : 15000,
    "Sate Ayam"  : 25000,
    "Soto Ayam"  : 25000,
    "Coto Makassar" : 30000,
    "Es Teh" : 5000,
    "Es Jeruk" : 6000,
    "Air Es" : 3000
}

def data_pengguna():
    "Memuat data pengguna dari CSV."
    users = {}
    try:
        with open(data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    username, password, role, gopay_balance = row
                    users[username] = {"password": password, "role": role, "saldo_gopay": int(gopay_balance)}
    except FileNotFoundError:
        pass
    return users

def simpan_data(users):
    "Menyimpan data pengguna ke CSV."
    with open(data_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for username, info in users.items():
            writer.writerow([username, info["password"], info["role"], info["saldo_gopay"]])

def register(users):
    "Mendaftarkan pengguna baru."
    print("\n=== Register ===")
    username = input("Username: ")
    if username in users:
        print("Username sudah digunakan. Coba username lain.")
        return None
    password = input("Password: ")
    role = "user"
    users[username] = {"password": password, "role": role, "saldo_gopay": 50000}
    simpan_data(users)
    print("Registrasi berhasil! Saldo awal GoPay: Rp50000")
    return username

def login(users):
    "Login pengguna."
    print("\n=== Login ===")
    username = input("Username: ")
    password = input("Password: ")
    if username == user_admin and password == pw_admin:
        print("Login berhasil sebagai Admin!")
        return username, "admin"
    elif username in users and users[username]["password"] == password:
        print("Login berhasil!")
        return username, users[username]["role"]
    else:
        print("Username atau password salah.")
        return None, None

def tampilkan_menu():
    """Menampilkan menu GoFood dalam format tabel."""
    table = PrettyTable(["No", "Item", "Harga"])
    for idx, (item, price) in enumerate(menu.items(), start=1):
        table.add_row([idx, item, f"Rp{price}"])
    print("\nDaftar Menu GoFood:")
    print(table)

def tampilkan_data_pengguna(users):
    """Menampilkan data pengguna dalam format tabel."""
    table = PrettyTable(["Username", "Role", "Saldo GoPay"])
    for username, info in users.items():
        table.add_row([username, info["role"], f"Rp{info['saldo_gopay']}"])
    print("\nData Pengguna:")
    print(table)

def pilih_menu():
    """Memilih menu GoFood."""
    while True:
        try:
            pilihan = int(input("\nPilih nomor menu yang ingin dipesan (0 untuk batal): "))
            if pilihan == 0:
                print("Pesanan dibatalkan.")
                return None
            elif 1 <= pilihan <= len(menu):
                item = list(menu.keys())[pilihan - 1]
                return item
            else:
                print("Nomor menu tidak valid, coba lagi.")
        except ValueError:
            print("Input harus berupa angka. Silakan coba lagi.")

def proses_pembayaran(users, username, harga):
    """Memproses pembayaran dengan GoPay."""
    if users[username]["saldo_gopay"] >= harga:
        users[username]["saldo_gopay"] -= harga
        simpan_data(users)
        print(f"Pembayaran berhasil. Sisa saldo GoPay Anda: Rp{users[username]['saldo_gopay']}")
        return True
    else:
        print(f"Saldo GoPay tidak mencukupi! Sisa saldo Anda: Rp{users[username]['saldo_gopay']}")
        return False
    
def cek_saldo(users, username):
    """Menampilkan saldo GoPay pengguna dalam format tabel."""
    table = PrettyTable(["Username", "Saldo GoPay"])
    saldo = users[username]["saldo_gopay"]
    table.add_row([username, f"Rp{saldo}"])
    print("\nCek Saldo:")
    print(table)

def tambah_saldo(users, username):
    """Menambahkan saldo GoPay."""
    try:
        jumlah = int(input("Masukkan jumlah saldo yang ingin ditambahkan: Rp"))
        users[username]["saldo_gopay"] += jumlah
        simpan_data(users)
        print(f"Saldo GoPay Anda berhasil ditambahkan. Saldo sekarang: Rp{users[username]['saldo_gopay']}")
    except ValueError:
        print("Input tidak valid! Saldo gagal ditambahkan.")

def menu_admin(users):
    """Menu admin untuk CRUD data menu dan saldo pengguna."""
    while True:
        print("\n=== Menu Admin ===")
        print("1. Tampilkan Menu")
        print("2. Tambah Item Menu")
        print("3. Hapus Item Menu")
        print("4. Tampilkan Data Pengguna")
        print("5. Ubah Saldo Pengguna")
        print("6. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_menu()
        elif pilihan == "2":
            item = input("Masukkan nama item baru: ")
            try:
                harga = int(input("Masukkan harga item baru: Rp"))
                menu[item] = harga
                print(f"{item} berhasil ditambahkan ke menu.")
            except ValueError:
                print("Harga harus berupa angka!")
        elif pilihan == "3":
            item = input("Masukkan nama item yang ingin dihapus: ")
            if item in menu:
                del menu[item]
                print(f"{item} berhasil dihapus dari menu.")
            else:
                print("Item tidak ditemukan dalam menu.")
        elif pilihan == "4":
            tampilkan_data_pengguna(users)
        elif pilihan == "5":
            user_to_update = input("Masukkan username pengguna: ")
            if user_to_update in users:
                try:
                    saldo_baru = int(input("Masukkan saldo baru: Rp"))
                    users[user_to_update]["saldo_gopay"] = saldo_baru
                    simpan_data(users)
                    print("Saldo berhasil diperbarui.")
                except ValueError:
                    print("Saldo harus berupa angka!")
            else:
                print("Pengguna tidak ditemukan.")
        elif pilihan == "6":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def menu_user(users, username):
    """Menu untuk pengguna dengan akses pemesanan biasa."""
    pesanan = []
    total_harga = 0

    while True:
        print("\n=== Menu User ===")
        print("1. Tampilkan Menu GoFood")
        print("2. Cek Saldo GoPay")
        print("3. Isi Saldo GoPay")
        print("4. Pesan Makanan")
        print("5. Lihat Semua Pesanan")
        print("6. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_menu()
        elif pilihan == "2":
            cek_saldo(users, username)
        elif pilihan == "3":
            tambah_saldo(users, username)
        elif pilihan == "4":
            tampilkan_menu()
            item_pilihan = pilih_menu()
            if item_pilihan is None:
                continue

            try:
                jumlah = int(input("Masukkan jumlah yang diinginkan: "))
                if jumlah <= 0:
                    print("Jumlah harus lebih dari 0.")
                    continue
            except ValueError:
                print("Input tidak valid, silakan masukkan angka.")
                continue
            
            harga = menu[item_pilihan]
            total_item_harga = harga * jumlah  
            total_harga += total_item_harga  

            print(f"\nAnda memilih {jumlah} {item_pilihan} dengan total harga Rp{total_item_harga}.")

            while True:
                lanjut = input("Apakah Anda ingin menambahkan pesanan lain? (y/n): ").lower()
                if lanjut == 'y':
                    tampilkan_menu()
                    item_pilihan = pilih_menu()
                    if item_pilihan is None:
                        continue

                    try:
                        jumlah = int(input("Masukkan jumlah yang diinginkan: "))
                        if jumlah <= 0:
                            print("Jumlah harus lebih dari 0.")
                            continue
                    except ValueError:
                        print("Input tidak valid, silakan masukkan angka.")
                        continue
                    
                    harga = menu[item_pilihan]
                    total_item_harga = harga * jumlah  
                    total_harga += total_item_harga  
                    print(f"\nAnda memilih {jumlah} {item_pilihan} dengan total harga Rp{total_item_harga}.")
                elif lanjut == 'n':
                    break
                else:
                    print("Input tidak valid, silakan coba lagi.")

            print(f"\nTotal harga pesanan Anda: Rp{total_harga}.")
            print("Memproses pembayaran...")

            if proses_pembayaran(users, username, total_harga):
                pesanan.append({"item": item_pilihan, "jumlah": jumlah, "total": total_harga})
                print("Mencari driver...")

                waktu_driver = random.randint(10, 30)
                print(f"Menunggu driver... (Estimasi waktu: {waktu_driver} detik)")
                time.sleep(waktu_driver)

                print("Driver ditemukan! Pesanan Anda akan segera diantar.")
            else:
                print("\nApakah Anda ingin menambah saldo? (y/n)")
                if input().lower() == 'y':
                    tambah_saldo(users, username)
                else:
                    print("Pembayaran gagal. Silakan coba lagi nanti.")

        elif pilihan == "5":
            print("\n=== Daftar Pesanan Anda ===")
            if not pesanan:
                print("Belum ada pesanan.")
            else:
                for order in pesanan:
                    print(f"Item: {order['item']}, Jumlah: {order['jumlah']}, Total: Rp{order['total']}")
        elif pilihan == "6":
            print("Terima kasih telah menggunakan GoFood dengan GoPay!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    users = data_pengguna()
    
    print("Selamat datang di GoFood\n")
    while True:
        print("\n=== Menu Utama ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            username, role = login(users)
            if username:
                if role == "admin":
                    menu_admin(users)
                elif role == "user":
                    menu_user(users, username)
        elif pilihan == "2":
            register(users)
        elif pilihan == "3":
            print("Terima kasih telah menggunakan aplikasi ini!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

main()
