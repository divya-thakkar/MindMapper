#define TRIGGERTHRESHOLD 800 

// the setup routine runs once when you press reset:
void setup() {
  pinMode(A0, INPUT); // read the input on analog pin 0:
  Serial.begin(9600); // initialize serial communication at 9600 bits per second:
  Serial.println("Setup Starting: ");
}

// the loop routine runs over and over again forever:
void loop() {
  
  int emgSignal = analogRead(A0);
  Serial.println(emgSignal);
  delay(1);  // delay in between reads for stability

  if(emgSignal > TRIGGERTHRESHOLD) {
    // trigger remote control button push
    Serial.println("******** REMOTE CONTROL BUTTON CLICK PUSHED*******");
    delay(1000);
  }
}