
# ----------------------------------------
import time
import math
import board
from git import Repo
from picamera2 import Picamera2
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

# ----------------------------------------
THRESHOLD = 15.0   # Shake sensitivity (m/s^2)
NAME = "SaS"

REPO_PATH = "/home/pi/FlatSatChallenge"
FOLDER_PATH = "/Images"

# -------------------- start --------------------
i2c = board.I2C()

accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(2)

print("System initialized. Waiting for shake...")

# -------------------- funcs --------------------
def git_push():
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote(name='origin')

        origin.pull()
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit("New shake-triggered photo")
        origin.push()

        print(" Photo pushed to GitHub.")
    except Exception as e:
        print(" GitHub push failed:", e)


def img_gen(name):
    timestamp = time.strftime("_%Y%m%d_%H%M%S")
    return f"{REPO_PATH}{FOLDER_PATH}/{name}{timestamp}.jpg"


def take_photo():
    while True:
        accelx, accely, accelz = accel_gyro.acceleration

        magnitude = math.sqrt(
            accelx**2 +
            accely**2 +
            accelz**2
        )

        if magnitude > THRESHOLD:
            print("\n PHOTO TRIGGERED BY SHAKE")
            print(f"Acceleration (m/s²):")
            print(f"  X: {accelx:.2f}")
            print(f"  Y: {accely:.2f}")
            print(f"  Z: {accelz:.2f}")
            print(f"  Magnitude: {magnitude:.2f}")

            time.sleep(1)  # debounce

            img_path = img_gen(NAME)
            picam2.capture_file(img_path)

            print(f"Saved file: {img_path}")

            git_push()

            print("Cooldown...\n")
            time.sleep(3)

        time.sleep(0.1)

# -------------------- MAIN --------------------
def main():
    take_photo()


if __name__ == "__main__":
    main()
