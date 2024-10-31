import random
import time
import csv
from prettytable import PrettyTable
import pwinput 

data_file = "data_pa.csv"

user_admin = "admin"
pw_admin = "admin123"

nama_driver = ["Agus", "Budiono", "Siregar", "Dewi", "Eko", "Fajar", "Gina", "Hana"]

menu = {
    "Nasi Goreng"   : 30000,
    "Ayam Geprek"   : 25000,
    "Bakso"         : 15000,
    "Mie Ayam"      : 20000,
    "Sate Ayam"     : 25000,
    "Soto Ayam"     : 25000,
    "Coto Makassar" : 30000,
    "Es Teh"        : 5000,
    "Es Jeruk"      : 6000,
    "Air Es"        : 3000
}

def memuatdata():
    user = {}
    try:
        with open(data_file, mode='r', newline='') as file:
            reader = csv.reader(file)
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
        for username, info in users.items():  # Corrected from users() to users.items()
            writer.writerow([username, info["password"], info["role"], info["saldo_gopay"]])

def register(users):
    print("\n=== Register ===")
    username = input("Username: ")
    if username in users:
        print("Username sudah digunakan. Coba username lain.")
        return None
    password = pwinput.pwinput("Password: ")
    role = "user"
    users[username] = {"password": password, "role": role, "saldo_gopay": 0}
    menyimpandata(users)
    print("Registrasi berhasil!")
    return username

def login(users):
    print("\n=== Login ===")
    username = input("Username: ")
    password = pwinput.pwinput("Password: ")
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
    table = PrettyTable(["No", "Item", "Harga"])
    for idx, (item, price) in enumerate(menu.items(), start=1):
        table.add_row([idx, item, f"Rp{price}"])
    print("\nDaftar Menu GoFood:")
    print(table)

def tampilkan_data_pengguna(users):
    table = PrettyTable(["Username", "Role", "Saldo GoPay"])
    for username, info in users.items():  
        table.add_row([username, info["role"], f"Rp{info['saldo_gopay']}"])
    print("\nData Pengguna:")
    print(table)

def pilih_menu():
    print("\nSilakan pilih menu dengan nomor yang sesuai:")
    tampilkan_menu()
    pilihan = int(input("\nMasukkan nomor menu yang ingin Anda pesan (0 untuk batal): "))
    if pilihan == 0:
        print("Pesanan dibatalkan.")
        return None
    elif 1 <= pilihan <= len(menu):
        nama_makanan = list(menu.keys())[pilihan - 1]
        return nama_makanan
    else:
        print("Nomor menu tidak valid, coba lagi.")

def proses_pembayaran(users, username, harga):
    if users[username]["saldo_gopay"] >= harga:
        users[username]["saldo_gopay"] -= harga
        menyimpandata(users)
        print(f"Pembayaran berhasil. Sisa saldo GoPay Anda: Rp{users[username]['saldo_gopay']}")
        return True
    else:
        print(f"Saldo GoPay tidak mencukupi! Sisa saldo Anda: Rp{users[username]['saldo_gopay']}")
        return False

def cek_saldo(users, username):
    table = PrettyTable(["Username", "Saldo GoPay"])
    saldo = users[username]["saldo_gopay"]
    table.add_row([username, f"Rp{saldo}"])
    print("\nCek Saldo:")
    print(table)

def tambah_saldo(users, username):
    try:
        jumlah = int(input("Masukkan jumlah saldo yang ingin ditambahkan: Rp"))
        users[username]["saldo_gopay"] += jumlah
        menyimpandata(users)
        print(f"Saldo GoPay Anda berhasil ditambahkan. Saldo sekarang: Rp{users[username]['saldo_gopay']}")
    except ValueError:
        print("Input tidak valid! Saldo gagal ditambahkan.")


def admin_menu(users):
    while True:
        table = PrettyTable()
        table.field_names = ["Menu Admin"]
        
        table.add_row(["1. Tampilkan Menu"])
        table.add_row(["2. Tambah Item Menu"])
        table.add_row(["3. Hapus Item Menu"])
        table.add_row(["4. Tampilkan Data"])
        table.add_row(["5. Mengubah Data"])
        table.add_row(["6. Keluar"])
        print(table)
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
            tampilkan_data_pengguna(users)
            ubah = input("Masukkan username pengguna yang ingin diubah: ")
            if ubah in users:   
                table = PrettyTable()
            table.field_names = ["Pilihan"]
            table.add_row(["1.  Ubah Username"])
            table.add_row(["2.  Ubah Saldo"])
            table.add_row(["3.  Kembali"])
            print(table)
            pilihan = input("Pilih Opsi: ")
            if pilihan == "1":
                    new_username = input("Masukkan username baru: ")
                    if new_username in users:
                        print("Username sudah digunakan. Coba username lain.")
                    else:
                        users[new_username] = users.pop(ubah)
                        print(f"Username berhasil diubah menjadi {new_username}.")
                        menyimpandata(users)
            elif pilihan == "2":
                    try:
                        saldo_baru = int(input("Masukkan saldo baru: Rp"))
                        users[ubah]["saldo_gopay"] = saldo_baru
                        menyimpandata(users)
                        print("Saldo berhasil diperbarui.")
                    except ValueError:
                        print("Saldo harus berupa angka!")
            elif pilihan == "3":
                    continue
            else:
                    print("Aksi tidak valid.")
        elif pilihan == "6":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def estimasi_waktu():
    return random.randint(5, 10)

def buat_invoice(username, pesanan, saldo_akhir):
    print("\n=== Invoice Pembayaran ===")
    table = PrettyTable(["Item", "Jumlah", "Harga Total"])

    for order in pesanan:
        table.add_row([order["item"], order["jumlah"], f"Rp{order['total']}"])

    print(table)
    print(f"Saldo GoPay Tersisa: Rp{saldo_akhir}")
    print("Terima kasih telah menggunakan GoFood!")

def user_menu(users, username):
    pesanan = []
    total_harga = 0

    while True:
        table = PrettyTable()
        table.field_names = ["Menu Pengguna"]
        table.add_row(["1. Tampilkan Menu GoFood"])
        table.add_row(["2. Cek Saldo GoPay"])
        table.add_row(["3. Isi Saldo GoPay"])
        table.add_row(["4. Pesan Makanan"])
        table.add_row(["5. Riwayat Pesanan"])
        table.add_row(["6. Keluar"])
        print(table)
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_menu()
        elif pilihan == "2":
            cek_saldo(users, username)
        elif pilihan == "3":
            tambah_saldo(users, username)
        elif pilihan == "4":
            while True:
                tampilkan_menu()
                makanan = pilih_menu()
                if makanan:
                    try:    
                        jumlah = int(input("Masukkan jumlah pesanan: "))
                        harga = menu[makanan]
                        total_harga += harga * jumlah
                        pesanlagi = input("Apakah anda ingin memesan lagi? "  "(y/t)")
                        pesanlagi == 't'
                        if proses_pembayaran(users, username, total_harga):
                            pesanan.append({"item": makanan, "jumlah": jumlah, "total": harga * jumlah})
                            saldo_akhir = users[username]["saldo_gopay"]
                            waktu_estimasi = estimasi_waktu()
                            driver = random.choice(nama_driver)
                            print(f"Driver {driver} mengambil pesanan Anda dalam waktu {waktu_estimasi} menit.")
                            time.sleep(2)
                            print(f"Driver telah mengantar pesanan Anda!")
                            time.sleep(2)
                            buat_invoice(username, pesanan, saldo_akhir)
                        total_harga = 0  
                        break
                    except ValueError:
                        print("Jumlah Pesanan harus berupa angka!")
                    else:
                        print("Pesanan dibatalkan")
        elif pilihan == "5":
            if pesanan:
                table = PrettyTable()
                table.field_names = ["Riwayat Pesanan"]
                for i, order in enumerate(pesanan, start=1):
                    table.add_row ([i,  order["item"], order["jumlah"], order["total"]])
                    print(table)
            else:
                print("Belum ada pesanan.")
        elif pilihan == "6":
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    users = memuatdata()

    while True:
        table = PrettyTable()
        table.field_names = ["Menu Utama"]
        table.add_row(["1. Login"])
        table.add_row(["2. Register"])
        table.add_row(["3. Keluar"])
        
        print(table)
        pilihan = input("Pilih opsi yang tersedia: ")

        if pilihan == "1":
            username, role = login(users)
            if username is None:
                continue
            
            if role == "admin":
                admin_menu(users)
            else:
                user_menu(users, username)

        elif pilihan == "2":
            username = register(users)
            if username is not None:
                user_menu(users, username)

        elif pilihan == "3":
            print("Terima kasih telah menggunakan aplikasi GoFood!")
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
