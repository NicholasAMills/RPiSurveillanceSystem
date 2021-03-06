'''
    @author:
        Nicholas Mills
        nicholas_mills@outlook.com
        completion date: Jan 17, 2020

    This project was built and tested using:
        Raspberry Pi 4 model B
        Raspberry Pi Camera V2 8MP
        HC-SR501 Adjust Ir Pyroelectric Infrared PIR Motion Sensor Detector Module
'''

from gpiozero import LED, MotionSensor
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from picamera import PiCamera
import os.path
from os import path
from datetime import datetime
from credentials import Login


# Variables
GREEN = LED(17)  # green LED is on GPIO pin 17
RED = LED(27)  # red LED is on GPIO pin 27
camera = PiCamera()
camera.framerate = 60
camera.resolution = (1920, 1080)
pir = MotionSensor(22)  # PIR motion sensor on GPIO pin 22

# Force LEDs off since if they're on while program is running before being told to turn off, they'll stay on
GREEN.off()
RED.off()

'''
    Starts at image0.jpg, and if the file already exists, increment the number by 1 until an available
    name is usable, then capture the image and store it under that name and return the directory
'''
def take_picture():
    # Checking if picture already exists
    counter = 0 # start at image0.jpg
    picture_exists = True # force loop to execute at least once (since do while loops don't exist in python)
    while picture_exists:
        if path.exists('RPiSurveillance/Captures/image%s.jpg' % counter): # if image# exists, increase the number
            counter += 1
        else:
            picture_exists = False
    camera.capture('RPiSurveillance/Captures/image%s.jpg' % counter) # capture and store picture
    capture_name = 'RPiSurveillance/Captures/image%s.jpg' % counter # store directory
    return capture_name # return directory to pass into send_email()

'''
    Upon successful try:
        Takes the filename and sends an email to myself with the image and the date/time the photo was taken. Returns
        True to set flag for green LED
    except:
        returns False to set flag for red LED

    Code referenced from:
        HowToFAQ
        https://bit.ly/2TAMKWe
'''
def send_email(filename):
    try:
        email_user = Login.get_username() # from sender (your email)
        email_password = Login.get_password() # your email password
        email_send = Login.get_recipient() # receiver's email

        subject = 'MOTION DETECTED' # email subject

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        now = datetime.now().strftime("%H:%M:%S on %B %d, %Y")
        body = "Motion detected at " + str(now) # email message
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, 'rb') # email attachment

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text) # server sends email
        server.quit() # quits server after email is sent
        print("Sent ", filename) # Debug: printing out image directory that was sent
        return True # if successful, return true
    except:
        return False


'''
    Main function. Waits for motion. Once motion is detected, it takes a picture, sends it
    to send_email, and if that goes through it turns the green LED on to indicate a
    success. Otherwise it turns the red LED on to indicate an error occured within the
    send_email function and then quit the program
'''
def main():
    # create directory
    try:
        os.makedirs("/home/pi/mu_code/RPiSurveillance/Captures/")
    except FileExistsError:
        pass
    while True:
        pir.wait_for_motion() # waits for motion
        if send_email(take_picture()): # If send_email passes, turn the green LED on
            GREEN.on()
            sleep(3)
            GREEN.off() # turn off after 3 seconds
        else:
            RED.on() # If send_email fails, turn on red LED
            quit() # If there's an error, quit the program
        pir.wait_for_no_motion() # wait for no motion to help prevent spam

# Call main function
main()
