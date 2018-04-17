# qr-filetransfer-universal
📁 Send files from your PC to your Phone through WiFi with a QR code

## About
This is a handy little python 3 program that allows you to send files or folders through your Local Area Network (inside your WiFi) by simply scanning a QR Code through your phone! The code is based off sdushantha's amazing work with some added stuff that I found useful plus compatibility with Windows aside from macOS and Linux.

*Note that on Windows, the QR Code won't appear inside the powershell/cmd window but instead through an image viewer.*

## Installation

Windows:

1. Install Python 3 if you don't have it.
2. Open powershell and execute:
    pip install pyqrcode
3. Download the qr-filetransfer-universal.py file from here
4. Run it!


Linux / macOS:
```bash
# clone the repo
> git clone https://github.com/sdushantha/qr-filetransfer.git

# install the requirements
> pip3 install -r requirements.txt
```


## Usage
Just double click the .py file and drag and drop inside whatever you want to send! Alternatively you can also use the program this way:

```
usage: qr-filetransfer.py [-h] -f FILE
```

**Note:** Both devices needs to be connected to the same network

**Exiting**

To exit the program, just press ```CTRL+C```. **Dont** press ```CTRL+Z```.

---

Transfer a single file
```bash
python3 qr-filetransfer.py -f /path/to/file.txt
```


Transfer a full directory. **Note:** the directory gets zipped before being transferred
```bash
python3 qr-filetransfer.py -f /path/to/directory/
```

## Credits
* Based off sdushantha's [qr-diletransfer](https://github.com/sdushantha/qr-filetransfer)
* Inspired by the Go project [qr-filetransfer](https://github.com/claudiodangelis/qr-filetransfer)


## License
MIT License

Copyright (c) 2018 CedArctic