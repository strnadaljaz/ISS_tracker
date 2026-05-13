#include "WriteSmooth.h"
#include <Arduino.h>
#include <ESP32Servo.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <string>

#define WAIT_TIME 10

int WriteSmooth(Servo& servo, int currentRotation, int endRotation) {
    for (int i = currentRotation; i != endRotation;) {
        servo.write(i);
        i += (currentRotation < endRotation) ? 1 : -1;
        Serial.print("Current: ");
        Serial.print(i);
        Serial.print('\n');
        delay(WAIT_TIME);
    }

    servo.write(endRotation);
    return endRotation;
}