// Uses Arduino internal Timer1 to interrupt every time
// x ms passes and calculates instantaneous velocity of
// rotary encoder at that time. Then compares velocity to 
// threshold, and if velocity is over threshold, 
// switches boolean variable to 1, else keeps
// boolean off.

// OPCODE DEFINITIONS FOR RECEIVING
// SERIAL COMMANDS
#define OK                    0xaa
#define TEST_CONNECTION       0x02
#define SET_THRESHOLD_MOVE    0x06
#define GET_THRESHOLD_MOVE    0x07
#define SET_THRESHOLD_STOP    0x08
#define GET_THRESHOLD_STOP    0x09
#define SET_SAMPLING_PERIOD   0x0a
#define GET_SAMPLING_PERIOD   0x0b
#define GET_SERVER_VERSION    0x0e
#define TEST                  0xee
#define ERROR                 0xff

#define VERSION        "0.1"

// ENCODER VARIABLES
// Cumulative encoder position counter
long positionCounter = 0;
// Previous encoder position
long lastPosition = 0;
// Instantaneous velocity of encoder
long velocity = 0;
// Time since Arduino was started in ms
long timeStamp = 0;
// Encoder output A pin
int outputA = 2;
// Encoder output B pin
int outputB = 4;
// Encoder output A pin state
int aState;
// Last state of encoder output A pin
int aLastState;

// BINARY OUTPUT VARIABLES
// Bool to track if mouse is running
boolean runState = 0;
// Pin for binary movement output
int binaryOutputPin = 13;
// Velocity threshold for moving recognition
int thresholdMove = 10;
// Velocity threshold for stop recognition
int thresholdStop = 1;
// Period to sample velocity in milliseconds
// MUST BE AN EVEN NUMBER
unsigned int samplingPeriod = 20;

// TIMER1 VARIABLES
// Timer1 counter value
const uint16_t t1_load = 0;
// Initialize Timer1 compare value
unsigned int t1_comp = samplingPeriod * 62.5;
// t1_comp = ((x * 0.001 * 16,000,000) / (256)) for a desired x 
// milliseconds to pass every counter increment (The constants
// simplify to 62.5)
// Examples:
// 125 > 2 ms
// 625 > 10 ms
// 32150 > 500 ms
// Note: Since 62.5 is odd, if samplingPeriod is an odd
// number, there will be an extra 0.5, and the timer
// will not be counting to exactly the time you want it
// to on every cycle. So only set samplingPeriod to be
// an even number.

// For receiving serial communications
unsigned char serialByte;

void setup() {
  
    // Setup pin for binary output
    pinMode(binaryOutputPin, OUTPUT);
    // Set binary output pin low
    digitalWrite(binaryOutputPin, LOW);
  
    // Set up input pins for rotary encoder
    pinMode(outputA, INPUT);
    pinMode(outputB, INPUT);
  
    Serial.begin(115200);
 
    // Set up Timer1
    setUpTimer1();
  
    // Reads the initial state of the outputA
    aLastState = digitalRead(outputA);

}

void loop() {
  
    // Reads the "current" state of the outputA
    aState = digitalRead(outputA);
       
    // If the previous and the current state of the outputA 
    // are different then a pulse occurred
    if (aState != aLastState) {
      timeStamp = millis(); 
      // If the outputB state is different to the outputA state, 
      // then the encoder is rotating clockwise.
      // Otherwise, it's rotating counterclockwise
      if (digitalRead(outputB) != aState) { 
        positionCounter ++;
      } else {
        positionCounter --;
      }
    
    // Print time and positionCounter to serial monitor
    // separated by a space
    Serial.print(timeStamp);
    Serial.print(" ");
    Serial.print(positionCounter);
    Serial.println();

    }
  
    // Updates the previous state of outputA with the current state
    aLastState = aState;
    
    // Define what to do if serial commands are sent from
    // Python client to Arduino
    while (Serial.available() > 0) {
    serialByte = Serial.read();
    switch(serialByte) {
      case TEST_CONNECTION: {
	Serial.write(OK);
	break;
      }
      case GET_SERVER_VERSION: {
        Serial.println(VERSION);
        break;
      } 
      case SET_THRESHOLD_MOVE: {
	thresholdMove = read_int32_serial();
	break;
      }
      case GET_THRESHOLD_MOVE: {
	Serial.println(thresholdMove);
	break;
      }
      case SET_SAMPLING_PERIOD: {
	samplingPeriod = read_int32_serial();* 
        t1_comp = samplingPeriod * (125 / 2);
        setUpTimer1();
	break;
      }
      case GET_SAMPLING_PERIOD: {
	Serial.println(samplingPeriod);
	break;
      }
    }
  }
  
}

ISR(TIMER1_COMPA_vect) {
  
    // Reset the timer counter
    TCNT1 = t1_load;
  
    // Calculate the velocity
    velocity = abs(positionCounter - lastPosition);
    // If the velocity is over the threshold:
    if (velocity > thresholdMove) {
      // Mouse is running
      runState = 1;
      // Set binary output pin high
      digitalWrite(binaryOutputPin, HIGH);
    }
    else {
      // Mouse isn't running
      runState = 0;
      // Set binary output pin low
      digitalWrite(binaryOutputPin, LOW);
    }
  
    // Update the last position to be the current position
    // for the next velocity calculation
    lastPosition = positionCounter;
 
}

void setUpTimer1() {
  
    // Stop interrupts
    cli();
  
    // Reset Timer1 control register A
    TCCR1A = 0;
  
    // Set Timer1 prescaler to 256
    TCCR1B |= (1 << CS12);
    TCCR1B &= ~(1 << CS11);
    TCCR1B &= ~(1 << CS10);
  
    // Reset Timer1 and set compare value
    TCNT1 = t1_load;
    OCR1A = t1_comp;
  
    // Enable Timer1 overflow interrupt
    TIMSK1 = (1 << OCIE1A);
  
    // Enable interrupts
    sei();
 
}

unsigned long read_int32_serial() {
  
    // Read four bytes and combine them (little endian order, LSB first)
    long value = 0;
    for (int ind=0; ind<4; ind++) {
      while (!Serial.available()) {}  // Wait for data
      serialByte = Serial.read();
        value = ((long) serialByte << (8*ind)) | value;
    }
    
    return value;
    
}
