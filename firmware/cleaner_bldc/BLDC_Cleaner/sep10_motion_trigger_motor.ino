#include <EEPROM.h>

#include <BTAddress.h>
#include <BTAdvertisedDevice.h>
#include <BTScan.h>
#include <BluetoothSerial.h>

#include <Wire.h>

BluetoothSerial SerialBT;

#define BUZZER        27
#define VBAT          34

#define BRAKE         26        //chan phanh chung cua 3 dong co

//khai bao chan dong co 1
#define DIR1          4         //chan tin hieu chuyen huong xoay dong co
#define PWM1          32        //chan truyen xung toc do xoay 
#define PWM1_CH       1         //khai bao kenh cua dong co


//khai bao cam bien motion
int pirPin = 12; //Arduino pin the PIR sensor is connected to

int motionStatus = 0; // variable to store the PIR sensor's motion status (high or low)
int pirState = 0; // variable to track the state change

int32_t motor_speed_X, motor_speed_Y;

long currentT, previousT_1, previousT_2 = 0;

void writeTo(byte device, byte address, byte value)
{
  Wire.beginTransmission(device);
  Wire.write(address);
  Wire.write(value);
  Wire.endTransmission(true);
}

void beep(){
  digitalWrite(BUZZER, HIGH);
  delay(70);
  digitalWrite(BUZZER, LOW);
  delay(80);
}

void save(){
  EEPROM.put(0, offsets);
  EEPROM.commit();
  EEPROM.get(0, offsets);
  if(offsets.ID1 == 99 && offsets.ID2 == 99 && offsets.ID3 == 99 && offsets.ID4 == 99){
    calibrating = true;
  }
  calibrating = false;
  Serial.println("calibrating off");
  beep();
}

void batteryVoltage(double voltage){
  //Serial.print("batt: "); Serial.println(voltage);
  if(voltage > 8 && voltage <= 9.5){
    digitalWrite(BUZZER, HIGH);
  }
  else{
    digitalWrite(BUZZER, LOW);
  }
}

//ham truyen tin hieu pwm vao kenh cua dong co
void pwmSet(uint8_t channel, uint32_t value){
  ledcWrite(channel, value);
}

//ham dieu khien dong co
void Motor_control(int sp){
  if(sp < 0){
    digitalWrite(DIR1, LOW);
  sp = -sp;
  }
  else{
    digitalWrite(DIR1, HIGH);
  }
  pwmSet(PWM1_CH, sp > 255 ? 255 : 255 - sp);
}


void setup(){
  // put your setup code here, to run once:
  Serial.begin(115200);
  SerialBT.begin("NHT-ESP32");      //ten thiet bi bluetooth
  Serial.begin(9600); // initialize the serial monitor
  pinMode(pirPin, INPUT); // set the Arduino pin that PIR sensor is connected to as an INPUT

  pinMode(BUZZER, OUTPUT);

  pinMode(BRAKE, OUTPUT);
  digitalWrite(BRAKE, HIGH);

  pinMode(DIR1, OUTPUT);
  ledcSetup(PWM1_CH, BASE_FREQ, TIMER_BIT);
  ledcAttachPin(PWM1, PWM1_CH);
  Motor1_control(0);

    delay(2000);
    digitalWrite(BUZZER, HIGH);
    delay(70);
    digitalWrite(BUZZER, LOW);
    angle_setup();
    
    Serial.println("Setup complete");
}

void loop() {
  // put your main code here, to run repeatedly:
  currentT = millis();
  motionStatus = digitalRead(pirPin); // read the PIR pin's current output (is it HIGH or LOW?)
   
    // if the motion status is HIGH
    if (motionStatus == HIGH) { 
      if (pirState == LOW ) {
        Serial.println("Motion Detected"); // print result to the serial monitor
        pirState = HIGH; // update the previous state to HIGH
        Motor_control(50);
      }
    }
    
    //or else if motion status is low
    else { 
      if (pirState == HIGH) {
        Serial.println ("Motion Ended"); //print result to the serial monitor
        pirState = LOW; // update the previous state to LOW
        Motor_control(0);
      }
    delay(100);  // optional delay to slow down the PIR sensor reading intervals
    }
}
