
import sys
import os
import csv
import asyncio
import json
from datetime import datetime
from bleak import BleakScanner, BleakClient
from PyQt5.QtWidgets import (QApplication, QWizard, QWizardPage, QLabel, QLineEdit, QVBoxLayout, QDateEdit, QPushButton, QComboBox, QMessageBox, QInputDialog)
from PyQt5.QtCore import QDate, QThread, pyqtSignal, QTimer, QObject
import hashlib
import time
import string
import random


# Load exercise configuration from a JSON file
EXERCISE_CONFIG = {
    "Dribbling in Figure 8": {
      "sensors": [1, 2, 3, 4, 5],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z",
        "ball_Accel_X",
        "ball_Accel_Y",
        "ball_Accel_Z",
        "ball_Gyro_X",
        "ball_Gyro_Y",
        "ball_Gyro_Z"
      ]
    },
    "Dribbling in Figure O": {
      "sensors": [1, 2, 3, 4, 5],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z",
        "ball_Accel_X",
        "ball_Accel_Y",
        "ball_Accel_Z",
        "ball_Gyro_X",
        "ball_Gyro_Y",
        "ball_Gyro_Z"
      ]
    },
    "Large Ball Bounce and Catch": {
      "sensors": [1, 2, 5],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z",
        "ball_Accel_X",
        "ball_Accel_Y",
        "ball_Accel_Z",
        "ball_Gyro_X",
        "ball_Gyro_Y",
        "ball_Gyro_Z"
      ]
    },
    "Hit Balloon Up": {
      "sensors": [1, 2],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z"
      ]
    },
    "Jumping Jack with Clap": {
      "sensors": [1, 2, 3, 4],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Forward Backward Spread Legs and Back": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Criss Cross with Clapping": {
      "sensors": [1, 2, 3, 4],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Criss Cross without Clapping": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Criss Cross (leg forward)": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Alternate Feet Forward Backward": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Skipping": {
      "sensors": [1, 2, 3, 4],
      "columns": [
        "timestamp",
        "right_hand_Accel_X",
        "right_hand_Accel_Y",
        "right_hand_Accel_Z",
        "right_hand_Gyro_X",
        "right_hand_Gyro_Y",
        "right_hand_Gyro_Z",
        "left_hand_Accel_X",
        "left_hand_Accel_Y",
        "left_hand_Accel_Z",
        "left_hand_Gyro_X",
        "left_hand_Gyro_Y",
        "left_hand_Gyro_Z",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Jumping Jack without Hands": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Jump with feet symmetrically": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Jump with feet asymmetrically": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Hop between lines": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Hopping forward one one leg": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Step down from height": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Step over an obstacle": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    },
    "Stand on one leg": {
      "sensors": [3, 4],
      "columns": [
        "timestamp",
        "right_leg_Accel_X",
        "right_leg_Accel_Y",
        "right_leg_Accel_Z",
        "right_leg_Gyro_X",
        "right_leg_Gyro_Y",
        "right_leg_Gyro_Z",
        "left_leg_Accel_X",
        "left_leg_Accel_Y",
        "left_leg_Accel_Z",
        "left_leg_Gyro_X",
        "left_leg_Gyro_Y",
        "left_leg_Gyro_Z"
      ]
    }
  }


# UUIDs and other data
UART_SERVICE_UUIDS = [
    ("Sense Right Hand", "8E400004-B5A3-F393-E0A9-E50E24DCCA9E", "8E400006-B5A3-F393-E0A9-E50E24DCCA9E"),
    ("Sense Left Hand", "6E400001-B5A3-F393-E0A9-E50E24DCCA9E", "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    ("Sense Right Leg", "7E400001-A5B3-C393-D0E9-F50E24DCCA9E", "7E400003-A5B3-C393-D0E9-F50E24DCCA9E"),
    ("Sense Left Leg", "6E400001-B5C3-D393-A0F9-E50F24DCCA9E", "6E400003-B5C3-D393-A0F9-E50F24DCCA9E"),
    ("Sense Ball", "9E400001-C5C3-E393-B0A9-E50E24DCCA9E", "9E400003-C5C3-E393-B0A9-E50E24DCCA9E"),
]
buffers = {i: "" for i in range(1, 6)}
start_times = {i: None for i in range(1, 6)}
sensor_data = {i: {"timestamp": None, "values": [None] * 6} for i in range(1, 6)}

csv_filename = ""
STOP_FLAG = False
error_counter = 0
MAX_ERRORS = 4

def generate_hashed_id(info):
    # Generate a random string
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Get the current timestamp
    timestamp = str(time.time())

    # Combine the information with the random string and timestamp
    input_str = f"{info}_{random_str}_{timestamp}"

    # Generate the hash
    hash_object = hashlib.sha256(input_str.encode('utf-8'))
    return hash_object.hexdigest()[:20]  # Use the first 20 characters of the hash

# Function to append the new record to the exercise JSON file
def append_to_exercise_record(date, record):
    filename = f'exercise_records_{date}.json'
    try:
        with open(filename, 'r') as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        records = []

    records.append(record)
    with open(filename, 'w') as f:
        json.dump(records, f, indent=4)

# Define global variable for selected exercise configuration
selected_exercise_config = None

class GuiUpdater(QObject):
    showMessageSignal = pyqtSignal(str)
    stopExerciseSignal = pyqtSignal()
    stopForErrorsSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def show_message(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec()

    def stop_exercise(self):
        ex.stopExercise()

gui_updater = GuiUpdater()
gui_updater.showMessageSignal.connect(gui_updater.show_message)
gui_updater.stopExerciseSignal.connect(gui_updater.stop_exercise)
gui_updater.stopForErrorsSignal.connect(gui_updater.show_message)

async def notification_handler(sender, data, sensor_id):
    global buffers, start_times, STOP_FLAG, error_counter, selected_exercise_config
    if STOP_FLAG:
        return
    if start_times[sensor_id] is None:
        start_times[sensor_id] = datetime.now()
    buffers[sensor_id] += data.decode('utf-8')
    buffer = buffers[sensor_id]
    while '\n' in buffer:
        line, buffer = buffer.split('\n', 1)
        buffers[sensor_id] = buffer
        if line.strip() == "":
            continue
        try:
            parts = line.split(',')
            if len(parts) != 6:
                raise ValueError(f"Incorrect number of values: {len(parts)}. Received line: {line}")
            imu_values = list(map(float, parts))
            elapsed_time = (datetime.now() - start_times[sensor_id]).total_seconds() * 1000
            sensor_data[sensor_id]["timestamp"] = elapsed_time
            sensor_data[sensor_id]["values"] = imu_values
            if all(sensor_data[i]["timestamp"] is not None and sensor_data[i]["values"][0] is not None for i in selected_exercise_config["sensors"]):
                timestamp = round(sensor_data[selected_exercise_config["sensors"][0]]["timestamp"], 3)
                row = [timestamp] + sum((sensor_data[i]["values"] for i in selected_exercise_config["sensors"]), [])
                if len(row) != len(selected_exercise_config["columns"]):
                    raise ValueError("Row has an incorrect number of values")
                with open(csv_filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)
                for i in selected_exercise_config["sensors"]:
                    sensor_data[i]["timestamp"] = None
                    sensor_data[i]["values"] = [None] * 6
        except ValueError as e:
            error_counter += 1
            print(f"Error: {e}. Received line: {line}")
            if error_counter >= MAX_ERRORS:
                QTimer.singleShot(0, gui_updater.stopExerciseSignal.emit)
                QTimer.singleShot(0, lambda: gui_updater.stopForErrorsSignal.emit("Bad data, stop and restart"))

async def connect_to_sensor(device, sensor_id, char_uuid):
    async with BleakClient(device) as client:
        if client.is_connected:
            print(f"Connected to {device.name}")
            await client.start_notify(char_uuid, lambda sender, data: asyncio.create_task(notification_handler(sender, data, sensor_id)))
            while not STOP_FLAG:
                await asyncio.sleep(0.5)

async def scan_and_connect():
    tasks = []
    devices = await BleakScanner.discover()
    connected_sensors = []
    for sensor in selected_exercise_config["sensors"]:
        name, service_uuid, char_uuid = UART_SERVICE_UUIDS[sensor-1]
        for device in devices:
            if device.name == name:
                tasks.append(connect_to_sensor(device, sensor, char_uuid))
                connected_sensors.append(name)
                break
    gui_updater.showMessageSignal.emit(f"Connected to: {', '.join(connected_sensors)}")
    await asyncio.gather(*tasks)


class AsyncRunner(QThread):
    updateStatus = pyqtSignal(str)
    sensorsConnected = pyqtSignal()

    async def scan_and_connect(self):
        await scan_and_connect()
        self.sensorsConnected.emit()
        self.updateStatus.emit("Sensors connected")

    def run(self):
        global STOP_FLAG
        STOP_FLAG = False
        self.updateStatus.emit("Connecting to sensors...")
        asyncio.run(self.scan_and_connect())

    def stop(self):
        global STOP_FLAG
        STOP_FLAG = True

class StartPage(QWizardPage):
    def __init__(self, parent=None):
        super(StartPage, self).__init__(parent)
        self.setTitle("Start Page")
        layout = QVBoxLayout()
        #self.setFixedSize(500, 400)
        self.school_name_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat('dd/MM/yyyy')
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel("School Name:"))
        layout.addWidget(self.school_name_input)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_input)
        self.setLayout(layout)

        # Register the fields
        self.registerField("school_name_input*", self.school_name_input)
        self.registerField("date_input", self.date_input)

    def initializePage(self):
        print(get_saved_school_name())
        self.school_name_input.setText(get_saved_school_name())
        print(get_saved_date())
        self.date_input.setDate(get_saved_date())

    def validatePage(self):
        save_school_name(self.school_name_input.text())
        save_date(self.date_input.date())
        return True

def save_school_name(name):
    with open('school_name.txt', 'w') as f:
        f.write(name)

def get_saved_school_name():
    try:
        with open('school_name.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def save_date(date):
    with open('date.txt', 'w') as f:
        f.write(date.toString('dd/MM/yyyy'))

def get_saved_date():
    try:
        with open('date.txt', 'r') as f:
            date_str = f.read()
            return QDate.fromString(date_str, 'dd/MM/yyyy')
    except FileNotFoundError:
        return QDate.currentDate()

class ExerciseSelectionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ExerciseSelectionPage, self).__init__(parent)
        self.setTitle("Exercise Selection Page")
        layout = QVBoxLayout()
        self.exercise_combo = QComboBox()
        self.exercise_combo.addItems(EXERCISE_CONFIG.keys())
        layout.addWidget(QLabel("Select an Exercise:"))
        layout.addWidget(self.exercise_combo)
        self.setLayout(layout)

    def validatePage(self):
        global selected_exercise_config
        exercise_name = self.exercise_combo.currentText()
        selected_exercise_config = EXERCISE_CONFIG[exercise_name]
        return True

class SensorConnectionPage(QWizardPage):
    def __init__(self, parent=None):
        super(SensorConnectionPage, self).__init__(parent)
        self.setTitle("Sensor Connection Page")
        layout = QVBoxLayout()
        self.status_label = QLabel("Status: Not connected")
        self.connect_button = QPushButton("Connect to Sensors")
        self.connect_button.clicked.connect(self.start_connection)
        layout.addWidget(self.status_label)
        layout.addWidget(self.connect_button)
        self.setLayout(layout)
        self.async_runner = AsyncRunner()
        self.async_runner.updateStatus.connect(self.update_status)
        self.async_runner.sensorsConnected.connect(self.on_sensors_connected)

    def start_connection(self):
        self.async_runner.start()

    def stop_connection(self):
        self.async_runner.stop()

    def update_status(self, status):
        self.status_label.setText(f"Status: {status}")

    def on_sensors_connected(self):
        self.wizard().next()

class ExercisePage(QWizardPage):
    def __init__(self, parent=None):
        super(ExercisePage, self).__init__(parent)
        self.setTitle("Exercise Page")
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.height_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.start_button = QPushButton("Start Exercise")
        self.stop_button = QPushButton("Stop Exercise")
        self.start_button.clicked.connect(self.start_exercise)
        self.stop_button.clicked.connect(self.stop_exercise)
        self.status_label = QLabel("Status: Waiting to start")
        layout.addWidget(QLabel("Student Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Height (cm):"))
        layout.addWidget(self.height_input)
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender_input)
        layout.addWidget(QLabel("Weight (kg):"))
        layout.addWidget(self.weight_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        print(self.ex().field("StartPage.school_name_input"))

    def validatePage(self):
        global student_info
        student_info = {
            "name": self.name_input.text(),
            "height": self.height_input.text(),
            "gender": self.gender_input.text(),
            "weight": self.weight_input.text()
        }
        return True

    def start_exercise(self):
        global csv_filename
        school_name = self.ex().field("StartPage.school_name_input")
        print(school_name)
        date = self.ex().field("StartPage.date_input")
        print(date)
        date_str = date.toString('ddMMyyyy')
        exercise_name = self.ex().field("ExerciseSelectionPage.exercise_combo")
        csv_filename = f"{school_name}_{date_str}_{exercise_name}.csv"
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(selected_exercise_config["columns"])
        self.status_label.setText("Status: Exercise started")

    def stop_exercise(self):
        global STOP_FLAG, student_info
        STOP_FLAG = True
        self.status_label.setText("Status: Exercise stopped")

        school_name = self.ex().field("StartPage.school_name")
        date = self.ex().field("StartPage.date").toString('dd/MM/yyyy')
        exercise_name = self.ex().field("ExerciseSelectionPage.exercise_combo")

        record = {
            "student_id": generate_hashed_id(student_info["name"]),
            "student_name": student_info["name"],
            "height": student_info["height"],
            "gender": student_info["gender"],
            "weight": student_info["weight"],
            "school_name": school_name,
            "date": date,
            "exercise_name": exercise_name,
            "csv_filename": csv_filename
        }

        append_to_exercise_record(date, record)
        gui_updater.showMessageSignal.emit("Exercise data has been saved.")

class ExerciseApp(QWizard):
    def __init__(self, parent=None):
        super(ExerciseApp, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setFixedSize(600, 500)

        self.start_page = StartPage(self)
        self.exercise_selection_page = ExerciseSelectionPage(self)
        self.sensor_connection_page = SensorConnectionPage(self)
        self.exercise_page = ExercisePage(self)

        self.addPage(self.start_page)
        self.addPage(self.exercise_selection_page)
        self.addPage(self.sensor_connection_page)
        self.addPage(self.exercise_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExerciseApp()
    ex.setWindowTitle("Exercise Wizard")
    ex.show()
    sys.exit(app.exec_())