# IoT ECG Analyzer

## Overview
The **IoT ECG Analyzer** is an Internet of Things (IoT) project designed to measure and analyze electrocardiogram (ECG) signals using the AD8232 sensor. This system enables the collection, processing, and monitoring of heart rate data in real-time, providing insights into potential abnormalities through fuzzy logic and sending notifications if needed.

## Features
- **Signal Collection**: Gathers ECG signals using the AD8232 sensor.
- **Real-Time Processing**: Uses the ESP8266 microcontroller to preprocess and send data to the cloud.
- **Cloud Integration**: Utilizes Firebase and MQTT for efficient data transmission and storage.
- **Node-RED Visualization**: Displays ECG data and analysis results via a web interface using WebSocket.
- **Abnormality Detection**: Implements fuzzy logic to classify heart rate conditions and notify users.
- **Notification System**: Sends email alerts for detected abnormalities.

## System Architecture
The project follows a modular architecture with the following key components:

1. **Hardware**:
    - **AD8232**: ECG sensor module for signal acquisition.
    - **ESP8266**: Microcontroller for signal preprocessing and cloud communication.

2. **Software**:
    - **Node-RED**: Used for visualizing real-time ECG data and analysis results.
    - **Firebase**: Cloud storage solution for ECG data.
    - **Fuzzy Logic**: Algorithm for detecting abnormalities in ECG signals.
    - **Web Interface**: Provides real-time visualization and user interaction.

## Workflow
1. The AD8232 sensor captures ECG signals.
2. The ESP8266 processes the raw signals and buffers them for efficient transmission.
3. Data is sent to Firebase via MQTT.
4. Node-RED fetches the data and displays it on a web-based dashboard.
5. Abnormal heart rate detection is performed using fuzzy logic.
6. Notifications are sent via email when abnormalities are detected.

## Installation
### Hardware Setup
1. Connect the **AD8232 sensor** to the **ESP8266 microcontroller**:
    - ECG Signal Output (AD8232) -> Analog Pin (ESP8266)
    - VCC (AD8232) -> 3.3V (ESP8266)
    - GND (AD8232) -> GND (ESP8266)

2. Ensure proper placement of electrodes for accurate ECG signal acquisition.

### Software Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/longnp54/IoT-ECG-Analyzer.git
   cd IoT-ECG-Analyzer
   ```
2. Configure the **ESP8266** firmware:
   - Open the Arduino IDE and install the required libraries (e.g., Firebase, MQTT).
   - Upload the provided ESP8266 code to your microcontroller.
3. Set up **Node-RED**:
   - Install Node-RED and required nodes for Firebase and WebSocket.
   - Import the provided Node-RED flow file (`node_red_flow.json`).
4. Configure **Firebase**:
   - Set up a Firebase project and replace the credentials in the ESP8266 code.
5. Run the system and access the web interface for real-time monitoring.

## Usage
1. Power on the device and ensure the AD8232 sensor is correctly attached to the user.
2. Open the web interface through the Node-RED dashboard.
3. Monitor the ECG signal and heart rate in real-time.
4. Check for email notifications if abnormalities are detected.

## Future Improvements
- Add support for multiple users.
- Integrate advanced machine learning algorithms for improved detection accuracy.
- Expand cloud integration to include more platforms like AWS or Azure.
- Optimize power consumption for portable use.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements
Special thanks to the contributors and open-source libraries used in this project.

---

Feel free to reach out for collaboration or questions regarding this project!
