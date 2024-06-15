# Uncomment this to pass the first stage
import socket
import threading
import sys

def request_handler(request_line, header, request_body):
    if request_line[0] == "GET" and request_line[1] == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif request_line[0] == "GET" and request_line[1].startswith("/echo"):
        response = request_line[1].split("/")[-1]
        encoding = header["Accept-Encoding"]
        if encoding.find("gzip") != -1:
            response = f"HTTP/1.1 200 OK\r\nContent-Encoding: {encoding}\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
    elif request_line[0] == "GET" and request_line[1] == "/user-agent":
        response = header["User-Agent"]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
    elif request_line[0] == "GET" and request_line[1].startswith("/files"):
        directory = sys.argv[2]
        response = request_line[1].split("/")[-1]
        try:
            with open(f"/{directory}/{response}", "r") as f:
                response = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    elif request_line[0] == "POST" and request_line[1].startswith("/files"):
        directory = sys.argv[2]
        response = request_line[1].split("/")[-1]
        with open(f"/{directory}/{response}", "w") as f:
            f.write(request_body)
        response = "HTTP/1.1 201 Created\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response

def client_handler(client, i):
    while True:
        request = client.recv(1024).decode("utf-8")
        print(f"Client {i} sent: {request}")
        request = request.split("\r\n")
        request_line = request[0].split(" ")
        headers = request[1:-1]
        flags = {}
        for header in headers:
            header = header.split(": ")
            flags[header[0]] = header[1]
        header = flags
        request_body = request[-1]
        response = request_handler(request_line, header, request_body)
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
        i += 1
    server_socket.close()


if __name__ == "__main__":
    main()
