// Important note: no strings in ANY of this!! Only ints!!
// This is for the mini version, i.e. just the arduino nano and co2 sensor

// Libraries
#include <Wire.h>
#include <Arduino.h>
#include "SparkFun_SCD4x_Arduino_Library.h" // Library for CO2 sensor

// Declaring objects from their resepctive classes
SCD4x scd41; // CO2 sensor; address: 0x62

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // CO2 sensor code
  scd41.begin();  

  delay(5000);
}

void loop() {
  // CO2 sensor code
  scd41.readMeasurement()
  float co2 = scd41.getCO2();

  delay(5000);
}
