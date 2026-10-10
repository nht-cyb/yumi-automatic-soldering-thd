// 2023-08-14: Used original Solder Feeder sketch and also XIAO touch example.
//          
// **    Think about making extrudeSpeed variable. 

#include <AccelStepper.h>
#include "Adafruit_FreeTouch.h"

const int qt_Threshold = 750;  // was 850 requires a semi-firm touch. 650 is OK, but might false?

const int stepPin = 4;
const int dirPin  = 5;
/* Used for chip that doesnt' have capacitive sensing
const int forwPin = 6; //Pin connected to the forward button
const int backPin = 7; //Pin connected to the backward button
*/

#define SpeedPin A2
int extrudeSpeed = 75; //Speed in steps/sec to move the motor (200 steps/rev)

// Touch pads
Adafruit_FreeTouch qt_1 = Adafruit_FreeTouch(A0, OVERSAMPLE_4, RESISTOR_50K, FREQ_MODE_NONE); // REV (was FWD)
Adafruit_FreeTouch qt_2 = Adafruit_FreeTouch(A1, OVERSAMPLE_4, RESISTOR_50K, FREQ_MODE_NONE); // FWD (was REV)

// Stepper
AccelStepper extruder(1, stepPin, dirPin); // (Type:driver(1 is default driver), STEP, DIR)
 
void setup()
{  
  Serial.begin(115200);

  // Initialize Stepper
  extruder.setMaxSpeed(1000);

  /* Used for chip that doesn't have capacitive sensing: 
     pinMode(forwPin, INPUT); // INPUT_PULLDOWN);
     pinMode(backPin, INPUT); // INPUT_PULLDOWN);
  */

  // Initialize Touch Pins
  if (! qt_1.begin())
    Serial.println("Failed to begin qt");
  if (! qt_2.begin())
    Serial.println("Failed to begin qt");
}

void loop()
{
  int qt1 = 0;
  int qt2 = 0;
  float Speed;
  int Action = 0;

  Speed = analogRead(SpeedPin); // 0 to 1023
  Serial.print(Speed); Serial.print("  ");
  extrudeSpeed = 50.0 * (1+ (Speed/1023));    // set range from 50 to 100
  
  /* Used for chip that doesn't have capacitive sensing:
     if (digitalRead(forwPin == HIGH) qt1 = 9999; else qt1 = 0;
     if (digitalRead(backPin == HIGH) qt2 = 9999; else qt2 = 0;
  */

  qt1 = qt_1.measure();
  qt2 = qt_2.measure();

  
  if (qt1 >= qt_Threshold)
  {
    extruder.setSpeed(extrudeSpeed);
    extruder.runSpeed();
    Action = 1;
  }
  else if (qt2 >= qt_Threshold)
  {
    extruder.setSpeed(-extrudeSpeed);
    extruder.runSpeed();
    Action = 2;
  }
  else 
  {
    extruder.setSpeed(0);
    extruder.stop();
    Action = 31;

  }
  Serial.print("Speed: "); Serial.print(extrudeSpeed); 
  Serial.print(" QT1: "); Serial.print(qt1); 
  Serial.print(" QT2: "); Serial.print(qt2); 
  Serial.print(" Action: "); Serial.print(Action); 
  Serial.println("");
  
  // delay(100); // **********************************
}
