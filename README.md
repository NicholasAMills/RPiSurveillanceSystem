# RPiSurveillanceSystem
#RPiSurveillanceSystem

This is a basic surveillance system that will take a picture when a pir motion sensor detects motion, and then send the image to a desired email. Upon success, a LED will be lit up for 3 seconds before turning off, ready to take another picture. If an error occurs, the other LED will be lit indefinitely and the program will quit.

Requirements:
Two (preferably) different colored LED's

Raspberry Pi Camera

Raspberry Pi with GPIO pins

PIR motion sensor

gmail account

Instructions:
1. Connect one color LED to GPIO pin 17. This will be your "success" light.

2. Connect the other color to GPIO pin 27. This will be your "failed" light.

3. Motion sensor: Double check pins! Remove the white cap to view which pin is what. Connect "out" to GPIO pin 22. Connect VCC pin to the 5v pin. Connect Gnd to ground.

4. Open "credentials.py" and type in your information. Keep this file safe as it will not hide your password in-editor! You do not need to touch anything in RPiSurveillance.py. Note: inside the "get_username()" function, you need a gmail account. The recipient does not need to be gmail if your primary email isn't through gmail. Otherwise, if gmail is your primary email, the "get_recipient()" should be your normal gmail account as that is where the images will be sent.

5. The current capture path is /home/pi/mu_code/Captures/ You will need to make a "Captures" folder inside the "mu_code" directory. This is where the photos taken will be stored.

6. Position device in desired location with camera and pir sensor facing same direction.

7. Run RPiSurveillance.py through any method you choose. (IDE, ssh server, terminal, etc.) Note: This program will run infinitely and will only end when you hit "stop" in the editor, ctrl+c in terminal (if ran through ssh server/terminal), or the raspberry pi is unplugged from power.
