import csv
import random
import time
from datetime import datetime
import os

def generate_data():
    """
    Generates a new row of dummy data for the rocket sensors.
    """
    rotation = random.uniform(0, 360)
    acceleration = random.uniform(0, 20)
    altitude = random.uniform(0, 5000)
    temperature = random.uniform(-50, 50)
    gps_latitude = random.uniform(-90, 90)
    gps_longitude = random.uniform(-180, 180)
    rocket_state = random.choice(['Idle', 'Pre-Launch', 'In Flight', 'Landing'])
    launch_status = random.choice(['Not Launched', 'Launched'])

    return [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        rotation, acceleration, altitude, temperature,
        gps_latitude, gps_longitude, rocket_state, launch_status
    ]

def run_data_generator(filename):
    """
    Continuously generates and appends new data to the CSV file.
    """
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write headers only if the file does not exist
            writer.writerow([
                "Timestamp", "Rotation", "Acceleration", "Altitude", "Temperature",
                "GPS_Latitude", "GPS_Longitude", "Rocket_State", "Launch_Status"
            ])
        try:
            while True:
                writer.writerow(generate_data())
                print("New data appended.")
                time.sleep(3)
        except KeyboardInterrupt:
            print("Data generation stopped.")
