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
    request = request.split(" ")
    if request[1] == "/":
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif request[1].startswith("/echo"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(request[1][6:])}\r\n\r\n{request[1][6:]}"
        client.sendall(response.encode("utf-8"))
    elif request[1] == "/user-agent":
        response = request[-1].split("\\")[0]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        client.sendall(response.encode("utf-8"))
    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    client.close()


if __name__ == "__main__":
    main()
