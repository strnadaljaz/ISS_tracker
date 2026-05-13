#include <Arduino.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <string>
#include "secrets.h"
#include "WriteSmooth.h"

bool getAltitudeAzimuthFromServer(int& altitude, int& azimuth);

Servo altitudeServo;
Servo azimuthServo;

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASS;

const std::string host = HOST; 
const std::string pathName = "/iss";
std::string url = host + ":8000" + pathName; 

HTTPClient http;

int altitudeServoOld = 90;
int azimuthServoOld = 90;

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

  // zacetni calibration
  altitudeServoOld = WriteSmooth(altitudeServo, altitudeServoOld, 180);
  altitudeServoOld = WriteSmooth(altitudeServo, altitudeServoOld, 0);

  azimuthServoOld = WriteSmooth(azimuthServo, azimuthServoOld, 180); 
  azimuthServoOld = WriteSmooth(azimuthServo, azimuthServoOld, 0);
}

void loop() {
  int altitude, azimuth; 
  bool isVisible = false;

  isVisible = getAltitudeAzimuthFromServer(altitude, azimuth);

  if (isVisible) {
    int altitudeToWrite = 90 + altitude;
    altitudeServoOld = WriteSmooth(altitudeServo, altitudeServoOld, altitudeToWrite);
    azimuthServoOld = WriteSmooth(azimuthServo, azimuthServoOld, azimuth);
  }
  else {
    altitudeServoOld = WriteSmooth(altitudeServo, altitudeServoOld, 90); 
    azimuthServoOld = WriteSmooth(azimuthServo, azimuthServoOld, 90); 
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

  else {
    String error = http.errorToString(httpCode);
    Serial.print("HTTP error: " + error);
  }

  http.end();

  return isVisible;
}