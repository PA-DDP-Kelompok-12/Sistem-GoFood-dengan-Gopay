import csv
import os

# Nama file CSV untuk menyimpan data pengguna
filename = 'users.csv'

# Memastikan file CSV ada
if not os.path.isfile(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password'])  # Menulis header

def register():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    # Memeriksa apakah username sudah ada
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                print("Username sudah terdaftar. Silakan coba lagi.")
                return

    # Menyimpan data pengguna ke file CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
        print("Registrasi berhasil! Silakan login.")

def login():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    # Memeriksa username dan password di file CSV
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                print("Login berhasil! Selamat datang, " + username)
                return
    print("Username atau password salah. Silakan coba lagi.")

def main():
    while True:
        print("\n1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        choice = input("Pilih opsi (1/2/3): ")

        if choice == '1':
            login()
        elif choice == '2':
            register()
            # Setelah registrasi, langsung masuk ke login
            login()
        elif choice == '3':
            print("Keluar dari program.")
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
