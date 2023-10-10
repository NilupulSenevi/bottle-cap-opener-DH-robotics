# server.py
import socket

def start_server():
    host = "192.168.1.15"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    print(f'Server started at {host}:{port}')
    try:
        while True:
            conn, addr = s.accept()
            print(f'Connected to {addr}')
            data = conn.recv(1024).decode('utf-8')
            if data == "TEST":
                conn.sendall("TEST_OK".encode('utf-8'))
            elif data == "OPEN_CAP":
                print("Opening the cap...")
                
                conn.sendall("DONE".encode('utf-8'))
            elif data == "CLOSE_CAP":
                print("Closing the cap...")
                conn.sendall("DONE".encode('utf-8'))
            conn.close()
    finally:
        s.close()

if __name__ == "__main__":
    start_server()