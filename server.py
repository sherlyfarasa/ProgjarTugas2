import socket
import os

def send_file(conn, filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            conn.sendall(data)
        print(f"File {filename} berhasil dikirim")
    except FileNotFoundError:
        conn.sendall(b"File tidak ditemukan")

def receive_file(conn, filename):
    try:
        with open(filename, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"File {filename} berhasil diterima")
    except:
        print("Terjadi kesalahan saat menerima file")

def remove_file(filename):
    try:
        os.remove(filename)
        print(f"File {filename} berhasil dihapus")
    except FileNotFoundError:
        print("File tidak ditemukan")
    except:
        print("Terjadi kesalahan saat menghapus file")

def list_files():
    files = os.listdir('.')
    return '\n'.join(files)

def get_file_size(filename):
    try:
        size = os.path.getsize(filename)
        size_mb = size / (1024 * 1024)
        return f"Ukuran file {filename}: {size_mb:.2f} MB"
    except FileNotFoundError:
        return "File tidak ditemukan"
    except:
        return "Terjadi kesalahan saat mendapatkan ukuran file"

def process_command(command, conn):
    if command.startswith("ls"):
        return list_files()
    elif command.startswith("rm"):
        filename = command.split(" ")[1]
        remove_file(filename)
    elif command.startswith("download"):
        filename = command.split(" ")[1]
        send_file(conn, filename)
    elif command.startswith("upload"):
        filename = command.split(" ")[1]
        receive_file(conn, filename)
    elif command.startswith("size"):
        filename = command.split(" ")[1]
        return get_file_size(filename)
    elif command.startswith("byebye"):
        return "byebye"
    elif command.startswith("connme"):
        return "connme"
    else:
        return "Perintah tidak valid"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Menunggu koneksi...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Terhubung dengan {addr}")

        while True:
            command = conn.recv(1024).decode()
            if not command:
                break

            result = process_command(command, conn)
            if result == "byebye":
                conn.sendall(b"Terima kasih! Sampai jumpa.")
                break
            elif result == "connme":
                conn.sendall(b"Terhubung kembali.")
            else:
                conn.sendall(result.encode())

        conn.close()
        print("Koneksi ditutup")

if __name__ == "__main__":
    main()