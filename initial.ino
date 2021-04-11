#include "DualVNH5019MotorShield.h"

DualVNH5019MotorShield md;
char incomingByte;

#define NUM_OF_SENSORS 1
#define startPin 3
#define trigPin 2 //attach pin D3 Arduino to pin Trig of HC-SR04
#define moveforward 400
#define moveleft 200
// defines variables
long duration[NUM_OF_SENSORS]; // variable for the duration of sound wave travel
int distance[NUM_OF_SENSORS]; // variable for the distance measurement


void stopIfFault()
{
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


void sendPulse(){
    // Clears the trigPin condition
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);
}


void move(char c)
{
  // forward
  if(c == 'w')
  {
    md.setSpeeds(-200,-200);
  }
  //backward
  if(c == 's')
  {
    md.setSpeeds(200,200);
  }
  //right
  if(c == 'd')
  {
    md.setSpeeds(-200,200);
  }
   //right
  if(c == 'a')
  {
    md.setSpeeds(200,-200);
  }
  if(c == 'p')
  {
    md.setBrakes(400, 400);
  }
  stopIfFault();
  delay(2);
}
 

void setup()
{
  Serial.begin(115200);
  //Serial.println("Dual VNH5019 Motor Shield");
  md.init();
  Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
  Serial.println("with Arduino UNO R3");
  digitalWrite(trigPin, LOW);
}

void q_stop()
{
  for (int i = 0; i < NUM_OF_SENSORS; ++i){
      sendPulse();
      // Reads the echoPin, returns the sound wave travel time in microseconds
       duration[i] = pulseIn(startPin + i, HIGH);
      // Calculating the distance
       distance[i] = duration[i] * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
       Serial.println(distance[i]);
       if (distance[i]<40 && distance[i]>1)
       {
        Serial.println("I stopped");
        move('p');
        for(int i=0; i<moveleft;i++)
      {
        move('a');
        delay(1);
      }
        
       }
  }
}

void loop()
{
  if(Serial.available())
    {
      incomingByte = Serial.read();
      if(incomingByte == '1')
      {
        md.setBrakes(400, 400);
        while(1);
      }
      for (int i = 0; i < NUM_OF_SENSORS; ++i){
      sendPulse();
      // Reads the echoPin, returns the sound wave travel time in microseconds
       duration[i] = pulseIn(startPin + i, HIGH);
      // Calculating the distance
       distance[i] = duration[i] * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
       Serial.println(distance[i]);
       if (distance[i]<50 && distance[i]>1 && incomingByte == 'w' )
       {
        Serial.println("I stopped");
        move('p');
        move('a');
        delay(5);
       }
       else
       {
        move(incomingByte);
       }
      
      }
 
      delay(2);
    }
    else
    {
      
      for(int i=0; i<moveforward;i++)
      {
        move('w');
        q_stop();
        delay(0.5);
        
      }
      for(int i=0; i<moveleft;i++)
      {
        move('a');
        q_stop();
        delay(1);
      }
    }
}





//void loop() {
//  // Displays the distance on the Serial Monitor
//  Serial.print("Distance: ");
//  for (int i = 0; i < NUM_OF_SENSORS; ++i){
//    sendPulse();
//    // Reads the echoPin, returns the sound wave travel time in microseconds
//    duration[i] = pulseIn(startPin + i, HIGH);
//    // Calculating the distance
//    distance[i] = duration[i] * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
//    Serial.print(distance[i]);
//    Serial.print(" ; ");
//  }
//  Serial.println(" cm");
//}    
//}
//void loop1()
//{
//  for (int i = 0; i <= 400; i++)
//  {
//    md.setM1Speed(i);
//    stopIfFault();
//    if (i%200 == 100)
//    {
//      Serial.print("M1 current: ");
//      Serial.println(md.getM1CurrentMilliamps());
//    }
//    delay(2);
//  }
//  
//  for (int i = 400; i >= -400; i--)
//  {
//    md.setM1Speed(i);
//    stopIfFault();
//    if (i%200 == 100)
//    {
//      Serial.print("M1 current: ");
//      Serial.println(md.getM1CurrentMilliamps());
//    }
//    delay(2);
//  }
//  
//  for (int i = -400; i <= 0; i++)
//  {
//    md.setM1Speed(i);
//    stopIfFault();
//    if (i%200 == 100)
//    {
//      Serial.print("M1 current: ");
//      Serial.println(md.getM1CurrentMilliamps());
//    }
//    delay(2);
//  }
//
//  for (int i = 0; i <= 400; i++)
//  {
//    md.setM2Speed(i);
//    stopIfFault();
//    if (i%200 == 100)
//    {
//      Serial.print("M2 current: ");
//      Serial.println(md.getM2CurrentMilliamps());
//    }
//    delay(2);
//  }
//  
//  for (int i = 400; i >= -400; i--)
//  {
//    md.setM2Speed(i);
//    stopIfFault();
//    if (i%200 == 100)
//    {
//      Serial.print("M2 current: ");
//      Serial.println(md.getM2CurrentMilliamps());
//    }
//    delay(2);
//  }
//  
//  for (int i = -400; i <= 0; i++)
//  {
//    md.setM2Speed(i);
//    stopIfFault();
//    if (i%200 == 100)
//    {
//      Serial.print("M2 current: ");
//      Serial.println(md.getM2CurrentMilliamps());
//    }
//    delay(2);
//  }
//}
