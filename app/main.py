# Uncomment this to pass the first stage
import socket
import threading
import sys
import gzip

def request_handler(request_line, header, request_body, sys_flags):
    # Some default variables
    encoding = header.get("Accept-Encoding") # For Encoding
    compressed = b""
    directory = sys_flags.get("--directory") # For Files
    # Index Response
    if request_line[0] == "GET" and request_line[1] == "/":
        print("Recieved Index Request")
        response = "HTTP/1.1 200 OK\r\n\r\n"
    # Echo Response or Gzip Echo Response
    elif request_line[0] == "GET" and request_line[1].startswith("/echo"):
        print("Recieved Echo Request",end=" ")
        response = request_line[1].split("/")[-1]
        if encoding is None or encoding.find("gzip") == -1:
            print("Without Gzip")
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        else:
            print("With Gzip")
            compressed = gzip.compress(response.encode("utf-8"))
            response = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(compressed)}\r\n\r\n"
    # User-Agent Response
    elif request_line[0] == "GET" and request_line[1] == "/user-agent":
        print("Recieved User-Agent Request")
        response = header.get("User-Agent")
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response)}\r\n\r\n{response}"
    # File Exists Response
    elif request_line[0] == "GET" and request_line[1].startswith("/files"):
        print("Recieved File Content Request")
        response = request_line[1].split("/")[-1]
        try:
            with open(f"/{directory}/{response}", "r") as f:
                response = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(response)}\r\n\r\n{response}"
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    # File Creation Response
    elif request_line[0] == "POST" and request_line[1].startswith("/files"):
        print("Recieved File Creation Request")
        print(sys.argv[2])
        response = request_line[1].split("/")[-1]
        with open(f"/{directory}/{response}", "w") as f:
            f.write(request_body)
            print("File Created")
        response = "HTTP/1.1 201 Created\r\n\r\n"
    # Invalid Response
    else:
        print("Recieved Invalid Request")
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    return response.encode("utf-8") + compressed

def client_handler(client, i, sys_flags):
    while True:
        request = client.recv(1024).decode("utf-8")
        print(f"Client {i} sent: {request}")
        request = request.split("\r\n")
        request_line = request[0].split(" ")
        print("Request Line: ", request_line)
        headers = request[1:-1]
        flags = {}
        for header in headers:
            header = header.split(": ")
            if len(header) != 2: continue
            flags[header[0]] = header[1]
        header = flags
        print("Headers: ", header)
        request_body = request[-1]
        print("Request Body: ", request_body)
        response = request_handler(request_line, header, request_body, sys_flags)
        client.sendall(response)
        print(f"Client {i} received: {response}")
    client.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Extracting argument flags
    sys_flags = {}
    print(sys.argv)
    if len(sys.argv) > 1 and len(sys.argv) % 2 == 0:
        print("System Flags Found")
        for i in range(1, len(sys.argv), 2):
            sys_flags[sys.argv[i]] = sys.argv[i+1]
    print("System Flags: ", sys_flags)
    
    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started")
    #server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n") # wait for client
    i = 1
    while True:
        client, address = server_socket.accept()
        print(f"Client {i} connected")
        threading.Thread(target=client_handler, args=(client,i,sys_flags)).start()
        i += 1
    server_socket.close()


if __name__ == "__main__":
    main()
