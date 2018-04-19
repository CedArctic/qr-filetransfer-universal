#!/usr/bin/env python3

import http.server
import socketserver
import random
import os
import socket
import argparse
import sys
from shutil import make_archive, move, rmtree, copy2
import pathlib

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def random_port():
    return random.randint(1024, 65535)


def start_server(fpath):

    # Select a Random Port Number and get the Local IP Address
    PORT = random_port()
    LOCAL_IP = get_local_ip()

    # Using tmp_qr as a temporary directory
    TEMP_DIR_NAME = "tmp_qr"

    # Remove quotation marks ("") from directory
    fpath = fpath.replace("\"", "")

    # Checking if given fname is a path
    if fpath.startswith("/"):
    	os.chdir("/")

    # Makes a directory named tmp_qr and stores the file there
    if os.path.isdir(TEMP_DIR_NAME):        # if the temporary directory exists already, delete it
        rmtree(TEMP_DIR_NAME)
    os.makedirs(TEMP_DIR_NAME)
    
    try:

        # Create an fname variable that will point to the new path that the file will be copied, remove spaces for windows compatibility
        # If fpath points to a file, fname will automatically get a file extension, if it is a directory, the .zip extension is added later on
        fname = fpath.replace(" ", "_")
        fname = os.path.basename(fname)
        zip_name = fname
        fname = TEMP_DIR_NAME + "/" + fname

        # Checking if given file name or path is a directory, if it is a directory, zip it and move the zip to the temporary directory
        if os.path.isdir(fpath):

            try:
                # Zips the directory
                path_to_zip = make_archive(zip_name, "zip", fpath)
                fpath = path_to_zip.replace(os.getcwd(), "")
                # The above line replacement leaves a / infront of the file name
                fpath = fpath[1:]
                #print(fpath)
                # Add .zip to fname, the destination path of the zip to be moved
                fname = fname + ".zip"
                move(fpath, fname)
            except PermissionError:
                print("PermissionError: Try with sudo")
                sys.exit()

        # If given path points to a file copy it to temporary directory
        else:
            # Copy the file to tmp_qr
            copy2(fpath, fname)

    except FileNotFoundError:
        print("File not found!")
        rmtree(TEMP_DIR_NAME)
        sys.exit()

    # Change our directory to .tmpqr
    os.chdir(TEMP_DIR_NAME)

    handler = http.server.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer(("", int(PORT)), handler)

    # This is the url to be encoded into the QR code
    address = "http://" + str(LOCAL_IP) + ":" + str(PORT) + "/" + os.path.basename(fname)

    print("\n")
    print("Server Address: " + address)     # Print server address and file name
    print("File name: " + os.path.basename(fname))
    print("\n")
    print("Scan the QR to start downloading. To quit just hit Ctrl+C.\nMake sure that your smartphone is connected to the same WiFi network as this computer.")
    print_qr_code(address, os.path.basename(fname))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        os.chdir("..")
        rmtree(TEMP_DIR_NAME)
        print("\nExiting...")
        sys.exit()


def print_qr_code(address, qrfname):

    if  os.name == 'nt':        # Check if the machine is running Windows
        import pyqrcode
        qrfname = "qr." + qrfname + ".png"
        qr = pyqrcode.create(address)
        if os.path.isfile(qrfname):  # Check if a qr.png exists, if yes, delete it so it can be replaced
            os.remove(qrfname)
        qr.png(qrfname, scale=5)
        os.system(qrfname)
        print("If you want the QR code picture, you can temporarily find it under the tmp_qr directory.\n\n")

    else:                       # If it isn't Windows it's a Unix based machine meaning qrcode module will do the trick of displaying the qr code within terminal
        import qrcode
        qr = qrcode.QRCode(1)
        qr.add_data(address)
        qr.make()
        qr.print_tty()


def main():
    parser = argparse.ArgumentParser(description = "\nTransfer files over WiFi from your computer to your mobile device by scanning a QR code.")

    parser.add_argument("-f", "--file",
			required=False,
			help="File to be shared")

    args = parser.parse_args()

    # If invalid agrument or no argument is given then prompt the user for input like this:
    if len(sys.argv) == 1:

        print("\nTransfer files over WiFi from your computer to your mobile device by scanning a QR code.")
        fpath = input("Enter the file/folder's directory or drag and drop it here and hit enter: ")

        # Remove quotation marks ("") from directory (in case the file path has spaces in it) and start server
        fpath = fpath.replace("\"" , "")
        start_server(fpath)

    else:

        start_server(fpath=args.file)

if __name__=="__main__":
	main()