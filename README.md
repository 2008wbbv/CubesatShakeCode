# CubesatShakeCode
Just some code

repo structure 

FlatSatChallenge/
│
├── Images/
│   └── (photos save here)
│
└── shake_cam.py

Install dependencies
sudo apt update
sudo apt install -y python3-picamera2 git
pip3 install adafruit-circuitpython-lsm6ds adafruit-circuitpython-lis3mdl gitpython

sudo raspi-config
Interface Options → Camera → Enable
Interface Options → I2C → Enable
Reboot when prompted

cd /home/pi
git clone https://github.com/2008wbbv/CubesatShakeCode
cd CubesatShakeCode

Configure Git identity
git config --global user.name "(user)
git config --global user.email "(email)"

vars: 
THRESHOLD = 15.0                 # Shake sensitivity
NAME = "YourName"                # Used in filename for photo 
REPO_PATH = "/home/pi/CubesatShakeCode
FOLDER_PATH = "/Images"

run: 
python3 shake_cam.py
