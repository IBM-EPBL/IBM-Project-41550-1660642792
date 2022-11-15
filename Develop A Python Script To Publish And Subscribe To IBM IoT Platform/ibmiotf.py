import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

organization = "0ooi4r"
devicetype = "Test_device"
deviceId = "262626"
authMethod = "token"
authToken = "hQXR(VA)Myh@UuMYAi"



def myCommandCallback(cmd):
    print("Command Received: %s" % cmd.data['command'])
    if status == "motoron":
        print(" m on")
    elif status == "motoroff":
        print("m off")
    elif status == "motor30":
        print("motor is on for 30 min")

try:

    deviceOptions = {"org": organization, "type": devicetype, "id": deviceId, "auth-method":authMethod, "auth-token": authToken}

    deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
    print("caught exception connecting device: %s" % str(e))
    sys.exit()

deviceCli.connect()

while True:

    temperature = random.randint(0,100)
    humidity = random.randint(0,100)
    soil_moisture = random.randint(0,100)

    data = {"temperature": temperature, "humidity": humidity, "soil_moisture": soil_moisture}

    def myOnPublicCallback():
        print("Published Temperature = %s c" % temperature, "Humidity = %s %%" % humidity, "soil_moisture = %s %%" % soil_moisture, "to IBM watson")

    success = deviceCli.publishEvent("IotSensor", "json", data, qos = 0, on_publish = myOnPublicCallback )
    if not success:
        print("Not connected to iotf")
    time.sleep(5)

    deviceCli.commandCallback = myCommandCallback

deviceCli.disconnect()
