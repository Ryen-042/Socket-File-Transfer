## Socket-File-Transfer
Transfer files and directories from one device to another using python sockets.

## Why this script?
One annoying thing is that I always need to copy one or more files from my laptop to my phone. There are some options as connecting my phone with a USB cable, but this is a pain, especially because I am always using all the USB ports, never mind that the cable itself is usually far from where I sit.

There are apps like shareit that share files. However, they are slow, unreliable, or take too many steps to begin the actual transfer process.

## Usage:
1- Activate the server: `python "server_main.py"`.

2- Run the client script. For this, you have two options:
  - Run this script normally and enter inputs as asked:  
    - `python "main_client.py"`
    
  - Use terminal arguments to skip the input steps:  
    - `python "main_client.py" [zip_filename] [files_or_directories]`
    
    For `files_or_directories`, provide one or more absolute paths separated by spaces.

## Bonus Section:
For entering file paths, you can drag-&-drop the file to the terminal, and the file path will be copied automatically. Also, some terminal programs allow dropping multiple files. One good example is [Cmder](https://cmder.app/).

---

If no connection could be established, the issue could be related to the firewall. For Windows users, you could solve it by:
  1. Open the start menu and search for: `Windows Defender Firewall with Advanced Security`.
  2. In the `Overview` section, click on `Windows Defender Firewall Properties`.
  3. Open the tap corresponding to your network type (`Private` or `Public`).
  4. From the `State` section, set the `Inbound connections` to `Allow`.

However, allowing all the inbound connections through the firewall is a security risk. So, instead, we can allow only specific connections through one or more ports by creating inbound rules:
  1. Same as above, open the start menu and search for: `Windows Defender Firewall with Advanced Security`.
  2. From the `Getting Started` section, click on `Inbound Rules`. You can also find it in the left sidebar.
  3. From the right `Action` sidebar, click on `New Rule`.
  4. Select the port option, then click on next.
  5. Specify the connection type to `TCP` and the `Port Number`.
