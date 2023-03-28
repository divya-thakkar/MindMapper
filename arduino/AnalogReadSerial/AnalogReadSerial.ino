#define NECKTHRESHOLD 200
#define JAWTHRESHOLD 200 

// the setup routine runs once when you press reset:
void setup() {
  pinMode(A0, INPUT); // read the input on analog pin 0:
  pinMode(A1, INPUT); // read the input on analog pin 1:
  Serial.begin(9600); // initialize serial communication at 9600 bits per second:
  Serial.println("EMG Movements Now Being Detected");
}

// the loop routine runs over and over again forever:
void loop() {
  
  int emgSignalJaw = analogRead(A0);
  int emgSignalNeck = analogRead(A3);
  //Serial.println(emgSignal);
  delay(1);  // delay in between reads for stability

  if(emgSignalJaw > JAWTHRESHOLD) {
    // trigger remote control button push
    Serial.println("Jaw Clench Detected");
    delay(1000);
  }

  if(emgSignalNeck > NECKTHRESHOLD) {
    // trigger remote control button push
    Serial.println("Neck Flex Detected");
    delay(1000);
  }
}