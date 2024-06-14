# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    #server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n") # wait for client
    client, address = server_socket.accept()
    request = client.recv(1024).decode("utf-8")
    request = request.split(" ")[1]
    if request == "/":
        server_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        server_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
