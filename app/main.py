# Uncomment this to pass the first stage
import socket
import threading

def request_handler(request_line, header):
    if request_line[1] == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif request_line[1].startswith("/echo"):
        response = request_line[1].split("/")[-1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
    elif request_line[1] == "/user-agent":
        response = header[1].split(": ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response

def client_handler(client, i):
    while True:
        request = client.recv(1024).decode("utf-8")
        print(f"Client {i} sent: {request}")
        request = request.split("\r\n")
        request_line = request[0].split(" ")
        header = request[1:-1]
        response = request_handler(request_line, header)
        client.sendall(response.encode("utf-8"))
        print(f"Client {i} received: {response}")
    client.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    #server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n") # wait for client
    i = 1
    while True:
        client, address = server_socket.accept()
        print(f"Client {i} connected")
        threading.Thread(target=client_handler, args=(client,i)).start()
    server_socket.close()


if __name__ == "__main__":
    main()
