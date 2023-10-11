// SPDX-FileCopyrightText: 2020 Carter Nelson for Adafruit Industries
//
// SPDX-License-Identifier: MIT
//
#include <Adafruit_APDS9960.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_LIS3MDL.h>
#include <Adafruit_LSM6DS33.h>
#include <Adafruit_SHT31.h>
#include <Adafruit_Sensor.h>
#include <PDM.h>
#include "MS5837.h"
#include <Wire.h>


Adafruit_APDS9960 apds9960; // proximity, light, color, gesture
Adafruit_BMP280 bmp280;     // temperautre, barometric pressure
Adafruit_LIS3MDL lis3mdl;   // magnetometer
Adafruit_LSM6DS33 lsm6ds33; // accelerometer, gyroscope
Adafruit_SHT31 sht30;       // humidity
MS5837 ms5837;

uint8_t proximity;
uint16_t r, g, b, c;
float temperature, pressure, altitude;
float magnetic_x, magnetic_y, magnetic_z;
float accel_x, accel_y, accel_z;
float gyro_x, gyro_y, gyro_z;
float humidity;
int32_t mic;
int leak;

extern PDMClass PDM;
short sampleBuffer[256];  // buffer to read samples into, each sample is 16-bits
volatile int samplesRead; // number of samples read



void setup(void) {
  Serial.begin(115200);

  pinMode(5, INPUT); 

  // initialize the sensors
  apds9960.begin();
  apds9960.enableProximity(true);
  apds9960.enableColor(true);
  bmp280.begin();
  lis3mdl.begin_I2C();
  lsm6ds33.begin_I2C();
  sht30.begin();
  PDM.onReceive(onPDMdata);
  PDM.begin(1, 16000);


//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(10000);                       // wait for a second
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  
  //DEPTH
  Wire.begin();

  // Initialize pressure sensor
  // Returns true if initialization was successful
  // We can't continue with the rest of the program unless we can initialize the sensor
//  while (!ms5837.init()) {
//    Serial.println("Init failed!");
//    Serial.println("Are SDA/SCL connected correctly?");
//    Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
//    Serial.println("\n\n\n");
//    //delay(5000);
//    digitalWrite(LED_BUILTIN, HIGH);
//    delay(3000);                       // wait for a second
//    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
//    delay(2000);                       // wait for a second
//  }

  ms5837.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)

}

void loop(void) {

  //DEPTH
//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(100);                       // wait for a second
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  
  // Update pressure and temperature readings
  ms5837.read();

  //Leak Sensor
  leak = digitalRead(5);
  
  proximity = apds9960.readProximity();
  while (!apds9960.colorDataReady()) {
    delay(5);
  }
  apds9960.getColorData(&r, &g, &b, &c);

  temperature = bmp280.readTemperature();
  pressure = bmp280.readPressure();
  altitude = bmp280.readAltitude(1013.25);

  lis3mdl.read();
  magnetic_x = lis3mdl.x;
  magnetic_y = lis3mdl.y;
  magnetic_z = lis3mdl.z;

  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  lsm6ds33.getEvent(&accel, &gyro, &temp);
  accel_x = accel.acceleration.x;
  accel_y = accel.acceleration.y;
  accel_z = accel.acceleration.z;
  gyro_x = gyro.gyro.x;
  gyro_y = gyro.gyro.y;
  gyro_z = gyro.gyro.z;

  humidity = sht30.readHumidity();

  samplesRead = 0;
  mic = getPDMwave(4000);

  Serial.print("Data:");
  Serial.print(leak);
  Serial.print(":");
  Serial.print(pressure); //atm?
  Serial.print(":");
  Serial.print(magnetic_x); //uTesla
  Serial.print(":");
  Serial.print(magnetic_y); //uTesla
  Serial.print(":");
  Serial.print(magnetic_z); //uTesla
  Serial.print(":");
  Serial.print(accel_x); //m/s^2
  Serial.print(":");
  Serial.print(accel_y); //m/s^2
  Serial.print(":");
  Serial.print(accel_z); //m/s^2
  Serial.print(":");
  Serial.print(gyro_x); //dps
  Serial.print(":");
  Serial.print(gyro_y); //dps
  Serial.print(":");
  Serial.print(gyro_z); //dps
  Serial.print(":");
  Serial.print(ms5837.pressure()); //mbar
  Serial.print(":");
  Serial.print(ms5837.depth()); //m
  Serial.println(":");


  
  delay(10);
}

/*****************************************************************/
int32_t getPDMwave(int32_t samples) {
  short minwave = 30000;
  short maxwave = -30000;

  while (samples > 0) {
    if (!samplesRead) {
      yield();
      continue;
    }
    for (int i = 0; i < samplesRead; i++) {
      minwave = min(sampleBuffer[i], minwave);
      maxwave = max(sampleBuffer[i], maxwave);
      samples--;
    }
    // clear the read count
    samplesRead = 0;
  }
  return maxwave - minwave;
}

void onPDMdata() {
  // query the number of bytes available
  int bytesAvailable = PDM.available();

  // read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;
}
