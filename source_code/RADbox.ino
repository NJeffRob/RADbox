// Important note: no strings in ANY of this when interfacing with python!!

// Libraries
#include <Arduino.h>
#include <Wire.h>
#include "SparkFun_SCD4x_Arduino_Library.h" // Library for CO2 sensor
#include <SensirionI2CSgp41.h> // Library for VOC sensor
#include <DFRobot_DHT20.h> // This is for the built in temp/hum sensor on the grove beginner kit
#include <U8x8lib.h> // library for the OLED display (for fun)

// Declaring objects from their resepctive classes
SCD4x scd41; // CO2 sensor; address: 0x62
SensirionI2CSgp41 sgp41; // VOC sensor; address: 0x59
DFRobot_DHT20 dht20; // Temp/hum sensor; address: 0x38
U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE); // OLED

// Required for sgp41 sensors NOx measurements
uint16_t conditioning_s = 10;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Start the sensors
  scd41.begin();  
  sgp41.begin(Wire);
  dht20.begin();

  // Start the OLED
  u8x8.begin();
  u8x8.setFlipMode(1);

  delay(6000);
}

void loop() {
  // Fun message on the OLED! Branding!
  u8x8.setFont(u8x8_font_lucasarts_scumm_subtitle_o_2x2_f);
  u8x8.setCursor(3, 3);
  u8x8.print("RADBox");

  // Getting CO2 measurements
  scd41.readMeasurement();
  float co2 = scd41.getCO2();

  // Getting voc/nox measurements
  uint16_t defaultRh = 0x8000;
  uint16_t defaultT = 0x6666;
  uint16_t srawVOC = 0;
  uint16_t srawNOx = 0;

  sgp41.measureRawSignals(defaultRh, defaultT, srawVOC, srawNOx);

  // Getting temp/humi measurements
  float temp, humi;
  temp = dht20.getTemperature();
  humi = dht20.getHumidity()*100;

  // The following is to test the arduino code; it prints out the collected values
  // Serial.println((String)"CO2: "+co2+" ppm;" " VOC: "+srawVOC+" ppm; NOx: "+srawNOx+" ppm; Temperature: "+temp+" C; Humidity: "+humi*100+" %RH");
  // Serial.println("");

  // Need to print lines to serial connection so that python can read it
  Serial.print(co2);
  Serial.print(",");
  Serial.print(srawVOC);
  Serial.print(",");
  Serial.print(srawNOx);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(humi);
  Serial.println();
  
  delay(5000); // the CO2 sensor cannot go faster than one measurement every 5 seconds, therefore we include this delay
}

