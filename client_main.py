import socket
import tqdm
import zipfile
from global_imports import *
from sys import argv

os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "archives"), exist_ok=True)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "archives"))

BUFFER_SIZE = 1024 * 100

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The IP address or hostname of the server (i.e., the receiver).
if os.name == 'nt':
    host = "192.168.1.71"
elif os.name == "posix":
    host = "192.168.1.70"
else:
    host = socket.gethostname()

# The server's port number.
port = 9777

console.print(f"[normal1]Connecting to '[normal2]{host}[/]:[normal2]{port}[/]'...[/]")
client_socket.connect((host, port))
console.print(f"[normal1]Connected to '[normal2]{host}[/]:[normal2]{port}[/]'.[/]")

if len(argv) > 1:
    zip_filename = argv[1].strip()
else:
    console.print("[normal1]Enter a name for the zip file:", end=" ")
    zip_filename = input().strip()

target_paths = []
if len(argv) > 2:
    target_paths.extend(argv[2:])
else:
    console.print("[normal1]Enter the [normal2]paths[/] to the [normal2]files[/] and [normal2]directories[/] you want to transfer (enter a [normal2]blank line[/] to continue):[/]")
    while True:
        path = input("> ").strip().strip('"').strip()
        if path == "":
            break
        target_paths.append(path)

# No compression, just archiving for easier transfer.
with zipfile.ZipFile(zip_filename + ".zip", "w", compression = zipfile.ZIP_STORED, compresslevel = 0) as zf:
    for target_path in target_paths:
        # A file
        if os.path.isfile(target_path):
            relative_filepath = os.path.normpath(target_path)
            zf.write(target_path, arcname=os.path.split(target_path)[1])
            continue
        
        # Else: A directory
        base_dir = os.path.split(target_path)[0]
        
        total_filecount = 0
        for root_dir, cur_dir, files in os.walk(target_path, topdown=True):
            total_filecount += len(files)
        
        display_progress_bar(1, max(total_filecount, 1), "")
        file_counter = 1
        for (dir_path, subdir_names, files) in os.walk(target_path, topdown=True):
            for file in files:
                file_relative_path = os.path.normpath(os.path.join(dir_path.split(base_dir)[-1].lstrip(os.sep), file))
                filesize = os.path.getsize(os.path.join(base_dir, file_relative_path))
                zf.write(os.path.join(base_dir, file_relative_path), arcname=file_relative_path)
                display_progress_bar(file_counter, total_filecount, file)
                file_counter += 1

console.print(f"[normal1]Filename: '[normal2]{zip_filename}.zip'[/][/]")

zip_file_path = os.path.join(os.getcwd(), zip_filename + '.zip')
filesize = os.path.getsize(zip_file_path)

client_socket.sendall((zip_filename  + ".zip" + "|" + str(filesize)).encode() + f"{'':<{BUFFER_SIZE-len((zip_filename  + '.zip' + '|' + str(filesize)).encode())}}".encode())

if filesize / 1024 / 1024 >= 1:
    string_filesize = f"{filesize/1024/1024:.2f} MB"
elif filesize / 1024 >= 1:
    string_filesize = f"{filesize/1024:.2f} KB"
else:
    string_filesize = f"{filesize} Bytes"
console.print(f"[normal1]Filesize: [normal2]{string_filesize}[/][/]")

trans_progress = tqdm.tqdm(desc=f"Sending {os.path.split(zip_file_path)[1]}", total=filesize, leave=False, unit="B", unit_scale=True, unit_divisor=1024)
with open(zip_file_path, "rb") as zf:
    bytes_left = filesize
    while bytes_left:
        bytes_read = zf.read(BUFFER_SIZE)
        
        # Use sendall to assure transimission in busy networks
        client_socket.sendall(bytes_read + bytes(f"{'':<{BUFFER_SIZE-len(bytes_read)}}", "utf-8")) # .encode()
        
        bytes_left -= len(bytes_read)
        
        # Update the progress bar
        trans_progress.update(len(bytes_read))

console.print("")
console.print("[normal1]Operation completed. Deleting the created zip file...[/]")
os.remove(zip_file_path)
console.print("[normal1]Closing the socket connection...[/]")
client_socket.close()
console.print("[normal1]Done.[/]")
