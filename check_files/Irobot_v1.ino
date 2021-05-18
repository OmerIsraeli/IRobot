/* Encoder Library - Basic Example
// * http://www.pjrc.com/teensy/td_libs_Encoder.html
// *
// * This example code is in the public domain.
// */

#include <Encoder.h>
#include "DualVNH5019MotorShield.h"

DualVNH5019MotorShield md;
char incomingByte;

#define TEST 1
#define MOTOR 1

// encoder
#define encPin1 18
#define encPin2 19
#define READS_PER_DEFREE 18

// ultrasonic
#define NUM_OF_SENSORS 3
#define trigPin 22
int distance[NUM_OF_SENSORS];
int sonar_pins[NUM_OF_SENSORS] = {23,24,25}; // left to right!
int sonar_degrees[NUM_OF_SENSORS]{30, 0, -30}; // degree from wall to robot. positive if wall to the left
int min_dist[NUM_OF_SENSORS] = {30, 50,30};
int turn_degrees[NUM_OF_SENSORS] = {150, 180, 210};
//old and stupid
int duration[NUM_OF_SENSORS];
#define startPin 9

// movement
#define MIN_DIST 50
#define TURN_IF_WALL 90
#define spd -100

// Change these two numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder myEnc(encPin1,encPin2);
//   avoid using pins with LEDs attached


//////////////////////////////shit
void stopIfFault()
{
  if(MOTOR){
    if (md.getM1Fault())
    {
      Serial.println("M1 fault");
      while(1);
    }
    if (md.getM2Fault())
    {
      Serial.println("M2 fault");
      while(1);
    }
  }
}


////////////////////////detection
void sendPulse(){
    // Clears the trigPin condition
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW); 
}

//returns index of last sonar that is lower than min dist
//otherwise -1
int getDist(){
  int flag = -1;
  if(TEST) Serial.print("Distance: ");
  for (int i = 0; i < NUM_OF_SENSORS; ++i){
    sendPulse();
    // Reads the echoPin, returns the sound wave travel time in microseconds
    distance[i] = pulseIn(sonar_pins[i], HIGH) * 0.034 / 2;
    // Calculating the distance
    if(TEST) Serial.print(distance[i]);
    if(TEST) Serial.print(" ; ");
    if (distance[i] < min_dist[i] && distance[i] > 0){
      flag = i;
    }
    delay(30);
  }
  if(TEST) Serial.print(" ||");
  return flag;
}

int detectWall(){
  // Displays the distance on the Serial Monitor
  if (TEST) Serial.print("Distance: ");
  for (int i = 0; i < NUM_OF_SENSORS; ++i){
    sendPulse();
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration[i] = pulseIn(startPin + i, HIGH);
    // Calculating the distance
    distance[i] = duration[i] * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
    if (TEST) Serial.print(distance[i]);
    if (TEST) Serial.print(" ; ");  
  }
  
  return distance[0];
}




//////////////////////////old move
void move(char c)
{
  if(MOTOR) {
    // forward
    if(c == 'w')
    {
      md.setSpeeds(-1*spd,-1*spd);
    }
    //backward
    if(c == 's')
    {
      md.setSpeeds(spd,spd);
    }
    //left
    if(c == 'a')
    {
      md.setSpeeds(spd,-1*spd);
    }
    if(c == 'p')
    {
      md.setBrakes(400, 400);
    }
    //stopIfFault();
    delay(2);
  }
}




///////////////////////////////rnadom movement


void moveRandomly(){
  if(MOTOR) move('w');
  int detect = detectWall();
  if(detect >= 0){
    //turn
    if(TEST){
     if (TEST) Serial.println("I turn");
    }
  }
  else{
      if (TEST) Serial.println("I drive");
  }
  delay(1);
}



////////////////////////// new_move

void new_move(char c, int degrees){

  int detect = getDist();
  if(detect >= 0){
    if(MOTOR) turn(turn_degrees[detect]);
    if(TEST){
     if (TEST) Serial.println("I turn");
    }
  }
  else{
      if (TEST) Serial.println("I drive");
      if(MOTOR) {
    // forward
    if(c == 'w')
    {
      md.setSpeeds(-1*spd,-1*spd);
    }
    //backward
    if(c == 's')
    {
      md.setSpeeds(spd,spd);
    }
    //left
    if(c == 'a')
    {
      turn(degrees);
    }
    if(c == 'p')
    {
      md.setBrakes(400, 400);
    }
    //stopIfFault()
  }

  }
  delay(1);
}

void moveTurnTo180(){
  move('w');
  int detect = getDist();
  if(detect >= 0){
    if(MOTOR) turn(turn_degrees[detect]);
    if(TEST){
     if (TEST) Serial.println("I turn");
    }
  }
  else{
      if (TEST) Serial.println("I drive");
  }
  delay(1);
}




void turn(int degrees){
  long oldPosition  = -999;
  long start = myEnc.read();
  if (TEST) Serial.print("start = ");
  if (TEST) Serial.println(start);
  md.setSpeeds(spd,-1*spd);
  long newPosition = -3;
  do{
    newPosition = myEnc.read();

    if (newPosition != oldPosition) {
    oldPosition = newPosition;
    if (TEST) Serial.print((newPosition - start)/READS_PER_DEFREE);
    if (TEST) Serial.println((newPosition - start)/READS_PER_DEFREE < degrees);
    }
  }while((newPosition - start)/READS_PER_DEFREE < degrees);
  md.setSpeeds(0,0);
}




void setup() {
  Serial.begin(9600);
  if(MOTOR) md.init();
  pinMode(encPin1, INPUT);
  pinMode(encPin2, INPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  digitalWrite(trigPin, LOW);
  for (int i = 0; i < NUM_OF_SENSORS; ++i){
    pinMode(sonar_pins[i], INPUT); // Sets the echoPin as an INPUT
  }
}



void loopV0(){
  while(true){
    int distance = detectWall();
    if(distance < MIN_DIST)
    {
      turn(TURN_IF_WALL);
    }
    md.setSpeeds(spd,spd);
    if (TEST) Serial.println("distance");
    if (TEST) Serial.println("done");
  }
}

void loop(){
  while(true){
    moveTurnTo180();
  }
}

void new_loop()
{
    while(true)
    {
     if(Serial.available()){
        input = Serial.read();
        move_car(input);
    }
    else
    {
        moveTurnTo180();
    }

}
