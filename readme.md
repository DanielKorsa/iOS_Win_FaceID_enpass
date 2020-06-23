# Enpass Password Manager Face ID for macOS

Use Face Id in your browser on macOS for easy and fast login.
Insted of  entering a Master Password in Enpass browser extension one could use this python script which would recognize your face (using opencv and face_recognition) based on sample facial images you provide. 

<img width="1158" alt="Screenshot 2020-06-23 at 14 16 04" src="https://user-images.githubusercontent.com/23553118/85402982-e7468a80-b55c-11ea-940b-a62b888b5100.png">

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Enpass 6.4.2 (668)
* Firefox 77.0.1
* macOS Catalania

### Installing

* Clone repo
* Make venv
* Install requirements.txt
* Put pictures(3 and more pictures) where you face can be clearly seen in /faces folder.
* In System Preferences/Security and Privacy/Camera give permission to script (to access your cam)
* In System Preferences/Security and Privacy/Accessability give permission to script
* In System Preferences/Security and Privacy/Screen Recording give permission to script
* Make sure that Enpass Shortcuts in your Browser is (cmd + /)

### How to use

* Run script
* Open Firefox & Enpass
* Go to Firefox and press Shortcut
* Script will recognize your face and unlock Enpass


## Contributing

Contributers are welcome to adapt this code for Windows and other password managers. Please open an issue first to discuss what you would like to do.


## Authors

* **Daniel Ko** 



## License

---

