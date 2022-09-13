import socket
import tqdm
from sys import argv
from traceback import print_exc
from global_imports import *

os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files"), exist_ok=True)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files"))

# Using ("0.0.0.0") as the server IP address makes the socket listen to all the IPv4 addresses that are on the local network.
SERVER_HOST = "0.0.0.0"
# SERVER_HOST = socket.gethostname()
# SERVER_HOST = "192.168.1.70"

SERVER_PORT = 9777
BUFFER_SIZE = 1024 * 100

# Staring a TCP socket.
console.print("[normal1]Server is [normal2]starting[/]...[/]")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the IP and PORT to the server.
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Server is listening, i.e., server is now waiting for the client to connected.
console.print(f"[normal1]Server is [normal2]listening[/] as '[normal2]{SERVER_HOST}[/]:[normal2]{SERVER_PORT}[/]'.[/]")
server_socket.listen(1) # Number of client connections to serve

console.print("[normal1]Waiting for a [normal2]client[/] to [normal2]connect[/]...")
client_socket, address = server_socket.accept()
console.print(f"[normal1]Connected to [normal2]'{address[0]}[/]:[normal2]{address[1]}[/]'.[/]")

# Receiving the filename and filesize data.
filename, filesize = client_socket.recv(BUFFER_SIZE).decode().strip().split("|")
filename = os.path.normpath(filename)
filesize = int(filesize)

if os.name == "posix":
    filename = os.path.normpath(filename.replace("\\", "/"))

console.print(f"[RECV] Receiving data for the [{filename.strip()}] file.")
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", filename)

# Receiving the actual file.
progress = tqdm.tqdm(range(filesize), f"Receiving {os.path.split(filename)[1]}", unit="B", unit_scale=True, unit_divisor=1024)
bytes_left = filesize
with open(filename, "wb") as file:
    while bytes_left:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        
        if bytes_left <= BUFFER_SIZE:
            bytes_read = bytes_read.strip(" ".encode())
        
        if len(bytes_read) == 0:
            break
        
        
        file.write(bytes_read)
        progress.update(len(bytes_read))
        bytes_left -= len(bytes_read)

console.print("")
console.print(f"[normal1]Operation completed. Closing the socket connection...[/]")
client_socket.close()
server_socket.close()
console.print("[normal1]Done.[/]")
