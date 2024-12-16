#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Ticker.h>

// Thông tin WiFi
// const char* ssid = "BM_HTVT";
// const char* password = "bmhtvt2019";

const char* ssid = "Long Thang";
const char* password = "88888888";

// Thông tin MQTT Broker
const char* mqtt_server = "broker.hivemq.com"; 
const char* mqtt_username = "longnp54";  
const char* mqtt_password = "Long913916@"; 
const char* topic = "ecg"; 

WiFiClient espClient;
PubSubClient client(espClient);

// Cấu hình buffer
#define BUFFER_SIZE 50
int ecgBuffer[BUFFER_SIZE];
int bufferIndex = 0;
unsigned long lastSampleTime = 0;
const unsigned long sampleInterval = 10; // 4ms

// Nút nhấn
#define PULLUP_PIN D5
volatile bool buttonPressed = false;
volatile bool measureEnabled = false;

// Ticker
Ticker measureTicker;

// ISR cho nút nhấn
void IRAM_ATTR handleButtonPress() {
  buttonPressed = true;
}

// Hàm kết nối WiFi
void setupWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Đang kết nối WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi đã kết nối!");
  Serial.println("Địa chỉ IP: " + WiFi.localIP().toString());
}

// Hàm kết nối MQTT
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Đang kết nối MQTT...");
    if (client.connect("d6f5eb13d06c4242881a0b32b8fc44c8.s1.eu.hivemq.cloud", mqtt_username, mqtt_password)) {
      Serial.println("Đã kết nối MQTT!");
      client.subscribe(topic); 
    } else {
      Serial.print("Thất bại, thử lại sau 5 giây. Lỗi: ");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

// Hàm callback MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0'; // Chuyển payload thành chuỗi
  //Serial.print("Nhận MQTT: ");
  //Serial.println((char*)payload);
}

// Hàm nén dữ liệu ECG bằng Delta Encoding
String compressDeltaEncoding(int* data, int length) {
  String compressed = "";
  int previousValue = data[0];
  compressed += String(previousValue) + ",";
  for (int i = 1; i < length; i++) {
    int delta = data[i] - previousValue;
    compressed += String(delta) + ",";
    previousValue = data[i];
  }
  compressed.remove(compressed.length() - 1);
  return compressed;
}

// Hàm đo tín hiệu ECG
void measureECG() {
  if (measureEnabled) {
    unsigned long currentMillis = millis();
    if (currentMillis - lastSampleTime >= sampleInterval) {
      lastSampleTime = currentMillis;
      int ecgValue = analogRead(A0); // Đọc tín hiệu từ chân A0
      ecgBuffer[bufferIndex++] = ecgValue;

      if (bufferIndex >= BUFFER_SIZE) {
        String compressedData = compressDeltaEncoding(ecgBuffer, BUFFER_SIZE);
        //Serial.print("Đang gửi dữ liệu: ");
        //Serial.println(compressedData);

        if (client.publish(topic, compressedData.c_str())) {
          //Serial.println("Dữ liệu ECG đã gửi thành công!");
        } else {
          //Serial.println("Gửi dữ liệu ECG thất bại!");
        }

        bufferIndex = 0; // Reset bộ đệm
      }
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(PULLUP_PIN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(PULLUP_PIN), handleButtonPress, FALLING);

  setupWiFi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Khởi động Ticker
  measureTicker.attach_ms(sampleInterval, measureECG);
}

void loop() {
  if (buttonPressed) {
    delay(50); // Xử lý chống dội nút
    if (digitalRead(PULLUP_PIN) == LOW) {
      measureEnabled = !measureEnabled; // Chuyển đổi trạng thái đo
      Serial.println(measureEnabled ? "Bắt đầu đo ECG" : "Dừng đo ECG");
    }
    buttonPressed = false;
  }

  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
}
