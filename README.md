# guiPassswordManager

<img src="https://raw.githubusercontent.com/SubrataSarkar32/guiPassswordManager/refs/heads/main/images/Gui.png" width="200">

guiPasswordManager is a portable password manager built in python. It stores everything locally in a json file with encryption. It uses industry standard encryption and decryption methods provided with the help of cryptography python package. At present random password generation is dependent on python's random package but soon it will be replaced with some industry standard approach. Since everything gets stored locally there are very less chances of password leakage.

## Screenshots

  #### Login Screen

  ![Login screen](https://raw.githubusercontent.com/SubrataSarkar32/guiPassswordManager/refs/heads/main/images/LoginScreen.png)

  #### Main Screen

  ![Main screen](https://raw.githubusercontent.com/SubrataSarkar32/guiPassswordManager/refs/heads/main/images/MainScreen.png)

  #### Add Password Screen

  ![Add Password screen](https://raw.githubusercontent.com/SubrataSarkar32/guiPassswordManager/refs/heads/main/images/AddPasswordScreen.png)

  #### View Password Screen

  ![view Password screen](https://raw.githubusercontent.com/SubrataSarkar32/guiPassswordManager/refs/heads/main/images/ViewPasswordScreen.png)

## Installation

1) Clone this repo with `git clone https://github.com/SubrataSarkar32/guiPassswordManager.git`
2) Create a venv with `python -m venv venv`
3) Activate the virtual environment:
    > Linux: `source ./venv/bin/activate`
    
    > Windows; `\venv\Scripts\activate`
4) Go to v2 folder. Install the requirements.
   ```
   cd v2
   pip install -r requirements.txt 
   ```
5) Run the the tkinter app. `python gpm_v2.py`

## Run Direct Executable

You can also download the .exe executable from release to run it directly on your Windows machine.
For Linux systems you can use Wine to run the .exe application on your system

Link to Release page: [Release](https://github.com/SubrataSarkar32/guiPassswordManager/releases)

## Usage Guide

On the first run you setup the master password. Remember the passsword you type in. Click on `Login` and your master password will be set. Now you can add passwords to store and view. To logout click on `Logout`. Usage videos will be updated soon

## Donation

If this project helped you you save your time. You can give me a cup of coffee. :)

You can donate via BHIM UPI


![Super sub](https://github.com/SubrataSarkar32/subratasarkar32.github.io/blob/master/images/Supersub(200x200).jpg?raw=true)


[![Donate](https://github.com/SubrataSarkar32/subratasarkar32.github.io/blob/master/images/bhimupi(100x15).jpg?raw=true)](upi://pay?pn=Subrata%20Sarakar&pa=9002824700%40upi&tn=Donation&am=&cu=INR&url=http%3A%2F%2Fupi.link%2F)

Scan this QR Code to open your UPI Payment App on your phone

![QR code](https://github.com/SubrataSarkar32/subratasarkar32.github.io/blob/master/images/qrpay.png?raw=true)
