import random
import time
import csv
from prettytable import PrettyTable
import pwinput 
from datetime import datetime


data_file = "data_pa.csv"
menu_file = "menu.csv"

user_admin = "admin"
pw_admin = "admin123"

nama_driver = ["Agus", "Budiono", "Siregar", "Dewi", "Eko", "Fajar", "Gina", "Hana"]

def init_files():
    while True:
        try:
            with open(menu_file, "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["nama_menu", "harga"])
            break
        except FileExistsError:
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat membuat file menu: {e}")
            continue

    while True:
        try:
            with open(data_file, "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password", "role", "saldo_gopay"])
            break
        except FileExistsError:
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat membuat file data: {e}")
            continue



def validasi_username(username):
    if not username.isalpha():
        print("Username hanya boleh terdiri dari huruf (alphabet) tanpa spasi.")
        return False
    if username == "":
        print("Username tidak boleh kosong!")
        return False
    return True

def validasi_input(input_data):
    if input_data.strip() == "":
        print("Input tidak boleh kosong atau hanya spasi!")
        return False
    return True

def memuatdata():
    user = {}
    while True:
        try:
            with open(data_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    if len(row) == 4:
                        username, password, pengguna, saldo_gopay = row
                        user[username] = {"password": password, "role": pengguna, "saldo_gopay": int(saldo_gopay)}
            return user
        except FileNotFoundError:
            init_files()
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")
            continue

def menyimpandata(users):
    while True:
        try:
            with open(data_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password", "role", "saldo_gopay"]) 
                for username, info in users.items(): 
                    writer.writerow([username, info["password"], info["role"], info["saldo_gopay"]])
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan data: {e}")
            continue

def baca_menu():
    menu = {}
    while True:
        try:
            with open(menu_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    menu[row['nama_menu']] = int(row['harga'])
            return menu
        except FileNotFoundError:
            init_files()
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat membaca menu: {e}")
            continue

def simpan_menu(menu):
    while True:
        try:
            with open(menu_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['nama_menu', 'harga'])
                writer.writeheader()
                for nama_menu, harga in menu.items():
                    writer.writerow({'nama_menu': nama_menu, 'harga': harga})
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan menu: {e}")
            continue

def register(users):
    while True:
        print("\n=================")
        print("|   REGISTER   |")
        print("================")
        username = input("Nama: ").strip()  
        if not validasi_username(username):  
            continue
        if username in users:
            print("NAMA SUDAH DIGUNAKAN!")
            continue
        password = pwinput.pwinput("Password: ")
        if not validasi_input(password):  
            continue
        role = "user"
        users[username] = {"password": password, "role": role, "saldo_gopay": 0}
        try:
            menyimpandata(users)
            print("REGISTRASI BERHASIL, SILAHKAN LOGIN!")
            return username
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan data pengguna: {e}")
            continue

def login(users):
    while True:
        print("\n================")
        print("|    LOGIN     |")
        print("================")
        username = input("Nama: ").strip()  
        if not validasi_username(username):  
            continue
        password = pwinput.pwinput("Password: ")
        if not validasi_input(password):  
            continue
        
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
            time.sleep(1)
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
            continue

def tampilkan_menu():
    while True:
        try:
            menu = baca_menu()
            table = PrettyTable()
            table.field_names = ["No", "Menu", "Harga"]
            for idx, (nama_menu, harga) in enumerate(menu.items(), 1):
                table.add_row([idx, nama_menu, f"Rp{harga}"])
            print(table)
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat menampilkan menu: {e}")
            continue

def tambah_menu():
    while True:
        try:
            menu = baca_menu()
            nama_menu = input("Masukkan nama menu baru: ")
            if nama_menu in menu:
                print("Menu sudah ada!")
                continue
            harga = int(input("Masukkan harga menu: Rp"))
            menu[nama_menu] = harga
            simpan_menu(menu)
            print(f"Menu {nama_menu} berhasil ditambahkan!")
            break
        except ValueError:
            print("Harga harus berupa angka!")
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat menambahkan menu: {e}")
            continue

def hapus_menu():
    while True:
        try:
            menu = baca_menu()
            tampilkan_menu()
            nama_menu = input("\nMasukkan nama menu yang ingin dihapus: ")
            if nama_menu in menu:
                del menu[nama_menu]
                simpan_menu(menu)
                print(f"Menu {nama_menu} berhasil dihapus!")
                break
            else:
                print("Menu tidak ditemukan!")
                continue
        except Exception as e:
            print(f"Terjadi kesalahan saat menghapus menu: {e}")
            continue

def ubah_menu():
    while True:
        try:
            menu = baca_menu()
            tampilkan_menu()
            nama_menu = input("\nMasukkan nama menu yang ingin diubah: ")
            if nama_menu in menu:
                nama_baru = input("Masukkan nama menu baru: ")
                harga_baru = int(input("Masukkan harga baru: Rp"))
                del menu[nama_menu]
                menu[nama_baru] = harga_baru
                simpan_menu(menu)
                print("Menu berhasil diubah!")
                break
            else:
                print("Menu tidak ditemukan!")
                continue
        except ValueError:
            print("Harga harus berupa angka!")
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat mengubah menu: {e}")
            continue

def pilih_menu():
    while True:
        try:
            menu = baca_menu()
            print("\nSilakan pilih menu dengan nomor yang sesuai:")
            tampilkan_menu()
            pilihan = int(input("\nMasukkan nomor menu yang ingin Anda pesan (0 untuk batal): "))
            if pilihan == 0:
                print("Pesanan dibatalkan.")
                return None
            elif 1 <= pilihan <= len(menu):
                nama_menu = list(menu.keys())[pilihan - 1]
                return nama_menu, menu[nama_menu]
            else:
                print("Nomor menu tidak valid!")
                continue
        except ValueError:
            print("Input harus berupa angka!")
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat memilih menu: {e}")
            continue

def ambil_harga(menu_item):
    return menu_item[1]

def sortir_termurah():
    while True:
        try:
            menu = baca_menu()
            daftar_menu = []
            for nama_menu, harga in menu.items():
                daftar_menu.append([nama_menu, harga])
            daftar_menu.sort(key=ambil_harga)
            table = PrettyTable()
            table.field_names = ["No", "Menu", "Harga"]
            nomor = 1
            for menu in daftar_menu:
                nama_menu = menu[0]
                harga = menu[1]
                table.add_row([nomor, nama_menu, f"Rp{harga}"])
                nomor += 1
            print("\nMenu (dari termurah):")
            print(table)
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat mengurutkan menu termurah: {e}")
            continue

def sortir_termahal():
    menu = baca_menu()
    daftar_menu = []
    for nama_menu, harga in menu.items():
        daftar_menu.append([nama_menu, harga])
    daftar_menu.sort(key=ambil_harga, reverse=True)
    table = PrettyTable()
    table.field_names = ["No", "Menu", "Harga"]
    nomor = 1
    for menu in daftar_menu:
        nama_menu = menu[0]
        harga = menu[1]
        table.add_row([nomor, nama_menu, f"Rp{harga}"])
        nomor += 1
    print("\nMenu (dari termahal):")
    print(table)

def admin_menu(users):
    while True:
        try:
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
        except Exception as e:
            print(f"Terjadi kesalahan saat menampilkan menu admin: {e}")
            continue

def kelola_user(users):
    while True:
        try:
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
        except Exception as e:
            print(f"Terjadi kesalahan saat menampilkan menu kelola user: {e}")
            continue

def tampilkan_data_user(users):
    while True:
        try:
            table = PrettyTable()
            table.field_names = ["Username", "Role", "Saldo"]
            for username, info in users.items():
                if info["role"] != "admin":  
                    table.add_row([username, info["role"], f"Rp{info['saldo_gopay']}"])
            print(table)
            break
        except Exception as e:
            print(f"Terjadi kesalahan saat menampilkan data user: {e}")
            continue

def ubah_username(users):
    while True:
        try:
            tampilkan_data_user(users)
            username_lama = input("\nMasukkan username yang ingin diubah: ")
            if username_lama in users and users[username_lama]["role"] != "admin":
                username_baru = input("Masukkan username baru: ")
                if username_baru not in users:
                    users[username_baru] = users.pop(username_lama)
                    menyimpandata(users)
                    print("Username berhasil diubah!")
                    break
                else:
                    print("Username baru sudah digunakan!")
                    continue
            else:
                print("Username tidak ditemukan!")
                continue
        except Exception as e:
            print(f"Terjadi kesalahan saat mengubah username: {e}")
            continue

def ubah_saldo(users):
    while True:
        try:
            tampilkan_data_user(users)
            username = input("\nMasukkan username yang ingin diubah saldonya: ")
            if username in users and users[username]["role"] != "admin":
                saldo_baru = int(input("Masukkan saldo baru: Rp"))
                users[username]["saldo_gopay"] = saldo_baru
                menyimpandata(users)
                print("Saldo berhasil diubah!")
                break
            else:
                print("Username tidak ditemukan!")
                continue
        except ValueError:
            print("Saldo harus berupa angka!")
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat mengubah saldo: {e}")
            continue

def topup_gopay(users, username):
    while True:
        try:
            jumlah = int(input("Masukkan jumlah top-up GoPay: Rp"))
            if jumlah > 0:
                users[username]["saldo_gopay"] += jumlah
                menyimpandata(users)
                print(f"Top-up berhasil! Saldo baru: Rp{users[username]['saldo_gopay']}")
                break
            else:
                print("Jumlah top-up harus lebih dari nol!")
        except ValueError:
            print("Input harus berupa angka!")
            continue
        except Exception as e:
            print(f"Terjadi kesalahan saat top-up GoPay: {e}")
            continue

def cek_saldo(username, users):
    while True:
        try:
            user_data = users.get(username)
            if not user_data:
                print("Pengguna tidak ditemukan.")
                return False  
            saldo_gopay = user_data["saldo_gopay"]
            print(f"\nSaldo GoPay Anda: Rp{saldo_gopay}")
            break  
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return False  


def estimasi_waktu():
    return random.randint(5, 20)
            
def proses_pembayaran(users, username, total_harga):
    while True:
        try:
            print("===========================")
            print("| PILIH METODE PEMBAYARAN |")
            print("===========================")
            print("1. COD (Cash on Delivery)")
            print("2. GoPay")

            pilihan = input("Pilih metode pembayaran (1 atau 2): ")
            
            if pilihan == "1":
                print("Anda memilih metode pembayaran COD.")
                print(f"\nTotal yang harus dibayar: Rp{total_harga}")
                print("Silahkan bayar saat barang diantar.")
                return "COD"  

            elif pilihan == "2":
                print("Anda memilih metode pembayaran GoPay.")
                saldo_gopay = users[username]["saldo_gopay"]
                print(f"Saldo GoPay Anda: Rp{saldo_gopay}")
                print(f"Total yang harus dibayar: Rp{total_harga}")

                if saldo_gopay >= total_harga:
                    konfirmasi = input("Konfirmasi pembayaran dengan GoPay (y/n): ").lower()
                    if konfirmasi == 'y':
                        users[username]["saldo_gopay"] -= total_harga
                        menyimpandata(users)
                        print("Pembayaran berhasil menggunakan GoPay!")
                        print(f"Sisa saldo GoPay Anda: Rp{users[username]['saldo_gopay']}")
                        return "GoPay"  
                    else:
                        print("Pembayaran dibatalkan.")
                        return None  
                else:
                    print("Saldo GoPay Anda tidak cukup!")
                    tambah_saldo = input("Apakah Anda ingin menambahkan saldo GoPay? (y/n): ").lower()
                    if tambah_saldo == 'y':
                        ubah_saldo(users)
                    else:
                        print("Silahkan pilih metode pembayaran lain atau tambahkan saldo.")
                        continue 

            else:
                print("Pilihan tidak valid. Silahkan pilih 1 atau 2.")
                continue

        except ValueError:
            print("Input tidak valid. Pastikan memasukkan angka yang benar.")
            continue
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            continue


def proses_pesanan(users, username):
    global pesanan
    pesanan = []
    total_harga = 0

    while True:
        table = PrettyTable()
        table.field_names = ["MENU PESAN"]
        table.add_rows([
            ["1. Tampilkan Menu (Termurah)"],
            ["2. Tampilkan Menu (Termahal)"],
            ["3. Pesan"],
            ["4. Kembali"],
        ])
        print(table)
        
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
                        metode_pembayaran = proses_pembayaran(users, username, total_harga)  
                        if metode_pembayaran and proses_pembayaran:
                            driver = random.choice(nama_driver)
                            waktu = estimasi_waktu()
                            print(f"\nMencari driver... \nDriver {driver} akan mengantarkan pesanan dalam {waktu} menit.")
                            time.sleep(2)
                            print("Driver sedang mengantar pesanan Anda...")
                            time.sleep(2)
                            print("Pesanan telah sampai!")
                            buat_invoice(username, users, total_harga, metode_pembayaran)  
                            return pilihan
                except ValueError:
                    print("Jumlah pesanan harus berupa angka!")
        elif pilihan == "4":
            return None
        else:
            print("Pilihan tidak valid!")

def buat_invoice(username, users, total_harga, metode_pembayaran):
    while True:
        try:
            user_data = users.get(username)
            if not user_data:
                print("Pengguna tidak ditemukan.")
                return False
            
            saldo_gopay = user_data["saldo_gopay"]

            print("===============================")
            print("            GOFOOD             ")
            print("===============================")
            print(f"Nama Pelanggan : {username}")
            print(f"Tanggal        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Metode Pembayaran: {metode_pembayaran}")
            print("-------------------------------")
            print("Pesanan:")
            for item in pesanan:
                print(f"{item['item']} (Jumlah: {item['jumlah']}) - Rp{item['total']}")
            print(f"\nTotal Harga    : Rp{total_harga}")

            if metode_pembayaran == "GoPay":
                print(f"Sisa Saldo GoPay : Rp{saldo_gopay}")
            print("===============================")
            time.sleep(1)
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return False


def main():
    init_files()
    users = memuatdata()
    while True:
        print("\n==================")
        print("|     GOFOOD     |")
        print("==================")
        print("| 1. Register    |")
        print("| 2. Login       |")
        print("| 3. Keluar      |")
        print("==================")

        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            register(users)
        elif pilihan == "2":
            username, role = login(users)
            if role == "admin":
                admin_menu(users)
            elif role == "user":
                while True:
                    table = PrettyTable()
                    table.field_names = ["MENU USER"]
                    table.add_rows([
                        ["1. Tampilkan Menu"],
                        ["2. Pesan Makanan"],
                        ["3. Cek Saldo GoPay"],
                        ["4. Top Up GoPay"],
                        ["5. Keluar"]
                    ])
                    print(table)

                    user_choice = input("Pilih menu: ")

                    if user_choice == "1":
                        tampilkan_menu()
                    elif user_choice == "2":
                        proses_pesanan(users, username)
                    elif user_choice == "3":
                        cek_saldo(username, users)
                    elif user_choice == "4":
                        topup_gopay(users, username)
                    elif user_choice == "5":
                        break
                    else:
                        print("Pilihan tidak valid!")
        elif pilihan == "3":
            print("Terima kasih, sampai jumpa lagi!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
