#include <Arduino.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include "secrets.h"
#include <string>

bool getAltitudeAzimuthFromServer(int& altitude, int& azimuth);

Servo altitudeServo;
Servo azimuthServo;

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASS;

const std::string host = HOST; 
const std::string pathName = "/iss";
std::string url = host + ":8000" + pathName; 

HTTPClient http;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WIFI");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  altitudeServo.attach(33);   
  azimuthServo.attach(14);

  altitudeServo.write(0);
  delay(500);
  altitudeServo.write(180);
  delay(500);
  azimuthServo.write(0);
  delay(500);
  azimuthServo.write(180);
  delay(500);
}

void loop() {
  int altitude, azimuth; 
  bool isVisible = false;

  isVisible = getAltitudeAzimuthFromServer(altitude, azimuth);

  if (isVisible) {
    altitudeServo.write(90 + altitude);
    azimuthServo.write(azimuth);
  }
  else {
    altitudeServo.write(90);
    azimuthServo.write(90);
  }
  delay(1000);
}

bool getAltitudeAzimuthFromServer(int& altitude, int& azimuth) {
  HTTPClient http;
  bool isVisible;

  http.begin(url.c_str());

  int httpCode = http.GET();

  if (httpCode > 0) {
    String payload = http.getString();

    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (!error) {
      azimuth = doc["az"];
      altitude = doc["el"];
      isVisible = doc["visible"];
    }
  }

  if (azimuth > 180)
    azimuth -= 180;

  http.end();

  return isVisible;
}