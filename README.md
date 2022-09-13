# Socket-File-Transfer
Transfer files and directories from one device to another using python sockets.

# Why this script?
One annoying thing is that I always need to copy one or more files from my laptop to my phone. There are some options as connecting my phone with a USB cable, but this is a pain, especially because I am always using all the laptop ports, never mind that the cable itself is usually far from where I sit.

There are apps like shareit that share files. However, they are slow, unreliable, or take too many steps to reach the transfer process.

# Usage:
1- Activate the server: `python "server_main.py"`.

2- Run the client script. For this, you have two options:
  - Run this script normally and enter inputs as asked:  
    `python "main_client.py"`
  - Use terminal arguments to skip the input steps:  
    `python "main_client.py" [zip_filename] [files_or_directories]`  
    For `files_or_directories`, provide one or more absolute paths separated by spaces.
