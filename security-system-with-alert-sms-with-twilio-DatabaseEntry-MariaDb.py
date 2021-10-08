import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import pymysql
import os
GPIO.setmode(GPIO.BOARD)                     #Set GPIO pin numbering 
GPIO.setwarnings(False)
TRIG = 10                                  #Associate pin 23 to TRIG
ECHO = 8                                  #Associate pin 24 to ECHO

print ("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(12,GPIO.OUT)



while True:
    
    GPIO.output(12,0)
    GPIO.output(TRIG, False)                 #Set TRIG as LOW
    time.sleep(1)
    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                 #Set TRIG as LOW

    while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse

    while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                #Saves the last known time of HIGH pulse 

    pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
    distance = round(distance, 2)            #Round to two decimal points
    a=0
    while distance > 2 and distance < 10:      #Check whether the distance is within range
        a=a+1
        db = pymysql.connect(
        host="localhost",
        user="anas",
        passwd="emad123",
        database="record1")
        mycursor = db.cursor()
        
        GPIO.output(12,True)
        time.sleep(1)
        if a==1:
            print ("DANGER")
            insertQuery = "INSERT INTO articles(customer) VALUES ('Intruder detected danger');"
            mycursor.execute(insertQuery)
            print("No of Record Inserted :", mycursor.rowcount)
            print("Inserted Id :", mycursor.lastrowid)
            db.commit()
            db.close()
            os.system('/home/pi/program/twilio/pushbullet.sh "Danger"')
            from twilio.rest import Client
            client = Client("ACcf6a37ba5c14229120ae9a76121e91ef", "a3ae3ce48b46e0a100c48d7bbad52a62")
            client.messages.create(to="+923168605380", 
                                   from_="+12602648042", 
                                   body="Danger some intruder found in the range!")
        GPIO.output(TRIG, False)
        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
            pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
            pulse_end = time.time()                #Saves the last known time of HIGH pulse 

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)
        

    
    print ("Distance:",distance,"cm")
cleanup()
