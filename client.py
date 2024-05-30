import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Koneksi berhasil dibuat dengan server.")

    while True:
        command = input("Silakan masukkan perintah (ls/rm/download/upload/size/byebye): ")

        if command == "byebye":
            client_socket.sendall(command.encode())
            print("Menutup koneksi.")
            break

        client_socket.sendall(command.encode())

        if command.startswith("download"):
            filename = command.split(" ")[1]
            receive_file(client_socket, filename)
        elif command.startswith("upload"):
            filename = command.split(" ")[1]
            send_file(client_socket, filename)
        else:
            result = client_socket.recv(1024).decode()
            print(f"Hasil: {result}")

    client_socket.close()

def send_file(client_socket, filename):
    try:
        with open(filename, 'rb') as file:
            data = file.read()
            client_socket.sendall(data)
        print(f"Berhasil mengunggah file {filename}.")
    except FileNotFoundError:
        print("File tidak ditemukan.")
    except:
        print("Terjadi kesalahan saat mengunggah file.")

def receive_file(client_socket, filename):
    try:
        with open(filename, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"Berhasil mengunduh file {filename}.")
    except:
        print("Terjadi kesalahan saat mengunduh file.")

if __name__ == "__main__":
    main()