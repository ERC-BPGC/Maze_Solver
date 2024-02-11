int t;

const int LFOR = 11;
const int LBACK = 10;
const int RFOR = 13;
const int RBACK = 12;


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

  if(t == 70){          //move  forward(all motors rotate in forward direction)
  digitalWrite(LFOR,HIGH);
  digitalWrite(RFOR,HIGH);

  digitalWrite(LBACK,LOW);
  digitalWrite(RBACK,LOW);
}


  else if(t == 66){   
     //move reverse (all  motors rotate in reverse direction)
  digitalWrite(LBACK,HIGH);
  digitalWrite(RBACK,HIGH);

  digitalWrite(LFOR,LOW);
  digitalWrite(RFOR,LOW);
}
  
else if(t == 76){      //turn LEFT (right side motors rotate in forward direction,  right side motors doesn't rotate)
  digitalWrite(RFOR,HIGH);

  digitalWrite(LFOR,LOW);
  digitalWrite(RBACK,LOW);
  digitalWrite(LBACK,LOW);
}   

else  if(t == 82){      //turn RT (right side motors rotate in forward direction, left  side motors doesn't rotate)
  digitalWrite(LFOR,HIGH);

  digitalWrite(RBACK,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
}

else if(t ==83){
        //STOP (all motors stop)
  digitalWrite(LFOR,LOW);
  digitalWrite(LBACK,LOW);
  digitalWrite(RFOR,LOW);
  digitalWrite(RBACK,LOW);
}
delay(100);
}
}

