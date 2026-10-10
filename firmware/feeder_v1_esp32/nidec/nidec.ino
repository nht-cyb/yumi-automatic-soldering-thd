/* simple speed & direction test sketch for Nidec 24H** brushless motors with integrated controller and encoder.

Ispriration, schematics etc:
https://www.hackster.io/mircemk/diy-aduino-one-axis-self-balancing-device-55e45b

for reference:
//https://forum.arduino.cc/t/20-30khz-pwm-on-arduino-uno/1148295
//https://forum.arduino.cc/t/how-to-get-20khz-pwm-on-pin-d9/132857/7
//https://forum.arduino.cc/t/self-balancing-reaction-wheel-problems-with-nidec-24h-055m020/1139918/4

Potmeter on A2
speed (pwm) pin on D9 (cannot be changed because of special PWM mode)
direction on D8

*/
const int potentiometerPin = A2;  // Potentiometer connected to analog pin A0

long value = 512;

void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT); 
  pinMode (8, OUTPUT);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  digitalWrite(A0, LOW);
  digitalWrite(A1, HIGH);

  analogWriteSAH_Init();


}

void loop() {
  // Read the potentiometer value
  int potValue = analogRead(potentiometerPin);
  value = potValue - 512;
  
  analogWriteSAH(map(abs(value), 0, 512, 800, 0));
  
  if(potValue < 512 ){
    digitalWrite(8, LOW);
  }
  else{
    digitalWrite(8, HIGH);
  }

}


void analogWriteSAH_Init( void )
{
  // Stop the timer while we muck with it

  TCCR1B = (0 << ICNC1) | (0 << ICES1) | (0 << WGM13) | (0 << WGM12) | (0 << CS12) | (0 << CS11) | (0 << CS10);
  
  // Set the timer to mode 14...
  //
  // Mode  WGM13  WGM12  WGM11  WGM10  Timer/Counter Mode of Operation  TOP   Update of OCR1x at TOV1  Flag Set on
  //              CTC1   PWM11  PWM10
  // ----  -----  -----  -----  -----  -------------------------------  ----  -----------------------  -----------
  // 14    1      1      1      0      Fast PWM                         ICR1  BOTTOM                   TOP
  
  // Set output on Channel A to...
  //
  // COM1A1  COM1A0  Description
  // ------  ------  -----------------------------------------------------------
  // 1       0       Clear OC1A/OC1B on Compare Match (Set output to low level).
  
  TCCR1A = 
      (1 << COM1A1) | (0 << COM1A0) |   // COM1A1, COM1A0 = 1, 0
      (0 << COM1B1) | (0 << COM1B0) | 
      (1 << WGM11) | (0 << WGM10);      // WGM11, WGM10 = 1, 0
  
  // Set TOP to...
  //
  // fclk_I/O = 16000000
  // N        = 1
  // TOP      = 799
  //
  // fOCnxPWM = fclk_I/O / (N * (1 + TOP))
  // fOCnxPWM = 16000000 / (1 * (1 + 799))
  // fOCnxPWM = 16000000 / 800
  // fOCnxPWM = 20000

  ICR1 = 799;
  
  // Ensure the first slope is complete

  TCNT1 = 0;
  
  // Ensure Channel B is irrelevant
  
  OCR1B = 0;
  
  // Ensure Channel A starts at zero / off
  
  OCR1A = 0;
  
  // We don't need no stinkin interrupts
  
  TIMSK1 = (0 << ICIE1) | (0 << OCIE1B) | (0 << OCIE1A) | (0 << TOIE1);

  // Ensure the Channel A pin is configured for output
  DDRB |= (1 << DDB1);

  // Start the timer...
  //
  // CS12  CS11  CS10  Description
  // ----  ----  ----  ------------------------
  // 0     0     1     clkI/O/1 (No prescaling)

  TCCR1B = 
      (0 << ICNC1) | (0 << ICES1) | 
      (1 << WGM13) | (1 << WGM12) |              // WGM13, WGM12 = 1, 1
      (0 << CS12) | (0 << CS11) | (1 << CS10);
}



void analogWriteSAH( uint16_t value )
{
  if ( (value >= 0) && (value < 800) )
  {
    OCR1A = value;
  }
}