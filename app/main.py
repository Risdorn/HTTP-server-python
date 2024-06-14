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
    request = request.split("\r\n")
    request_line = request[0].split(" ")
    header = request[1:-1]
    if request_line[1] == "/":
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif request_line[1].startswith("/echo"):
        response = request_line[1].split("/")[-1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        client.sendall(response.encode("utf-8"))
    elif request_line[1] == "/user-agent":
        response = header[1].split(": ")[1]
        print(response)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        client.sendall(response.encode("utf-8"))
    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    client.close()


if __name__ == "__main__":
    main()
