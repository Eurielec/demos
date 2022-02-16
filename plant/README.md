# Plant

## Requirements

- Bluetooth.
- Linux. MacOS not compatible with bluepy.
- `libgtk2.0-dev` installed for bluepy. You can do so by `sudo apt install libgtk2.0-dev`.

## Permissions

Because this demo uses BLE, it needs root to access it. That is why the install takes place on root.

## Install

1. Clone the repository with `git clone https://github.com/Eurielec/demos.git`
2. Go to the plant folder `cd demos/plant`
3. Install python3 and pip3 by `sudo apt install python3 python3-pip`.
4. Install dependencies with `sudo pip3 install -r requirements.txt`.
5. Fill the `.fill.env` with your values. Ask for them around at Eurielec.
6. Rename `.fill.env` to `.env` by running `mv .fill.env .env`
7. Run by `sudo python3 main.py`.
