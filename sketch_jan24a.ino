int t;

const int LFOR = 11;
const int LBACK = 10;
const int RFOR = 9;
const int RBACK = 6;

//delay timing
const int Spin_D_R = 205;
const int Spin_D_L = 198;
const int Line_D = 315;
const int Orient_D = 60;


void setup() {
  pinMode(LFOR,OUTPUT);   //left motors  forward
  pinMode(LBACK,OUTPUT);   //left motors reverse
  pinMode(RFOR,OUTPUT);   //right  motors forward-+
  pinMode(RBACK,OUTPUT);   //right motors reverse
  Serial.begin(9600);
}

void loop() {
if(Serial.available()){
  t = Serial.read();

  Serial.println("INSTRUCTION: ");
  Serial.println(t);

  Serial.print("\n");

  if(t == 55){          //move  forward(all motors rotate in forward direction)
  digitalWrite(LFOR,HIGH);
  digitalWrite(RFOR,HIGH);

  digitalWrite(LBACK,LOW);
  digitalWrite(RBACK,LOW);

  delay(Line_D);

  // digitalWrite(RFOR,HIGH);
  // digitalWrite(LBACK,HIGH);

  // digitalWrite(LFOR,LOW);
  // digitalWrite(RBACK,LOW);

  // delay(Orient_D);

  digitalWrite(LFOR,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
  digitalWrite(RBACK,LOW);
}


  else if(t == 54){   
     //move reverse (all  motors rotate in reverse direction)
  digitalWrite(LBACK,HIGH);
  digitalWrite(RBACK,HIGH);

  digitalWrite(LFOR,LOW);
  digitalWrite(RFOR,LOW);

  delay(Line_D);

  digitalWrite(LFOR,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
  digitalWrite(RBACK,LOW);
}
  
else if(t == 53){      //turn LEFT (right side motors rotate in forward direction,  left side motors rotate backward)
  digitalWrite(RFOR,HIGH);
  digitalWrite(LBACK,HIGH);

  digitalWrite(LFOR,LOW);
  digitalWrite(RBACK,LOW);

  delay(Spin_D_L);

  digitalWrite(LFOR,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
  digitalWrite(RBACK,LOW);
}   

else  if(t == 52){      //turn RT (left side motors rotate in forward direction,  right side motors rotate backward)
  digitalWrite(LFOR,HIGH);
  digitalWrite(RBACK,HIGH);
  
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);

  delay(Spin_D_R);

  digitalWrite(LFOR,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
  digitalWrite(RBACK,LOW);
}

else if(t == 51){
        //STOP (all motors stop)
  digitalWrite(LFOR,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
  digitalWrite(RBACK,LOW);
}
delay(100);
}
}

