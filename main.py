from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from time import sleep
from sys import exit

from BAC0.core.devices.local.object import ObjectFactory
from bacpypes.basetypes import DeviceObjectPropertyReference, DailySchedule, TimeValue
from bacpypes.constructeddata import ArrayOf
from bacpypes.object import ScheduleObject
from bacpypes.primitivedata import Real
from BAC0 import lite
from BAC0.core.devices.local.models import (
    analog_input,
    analog_output,
    binary_output,
    binary_input,
)



    
IPAdresse="160.221.49.52/25"
Port=47808
deviceId=22
sleepTime=5
# Define device
device = lite(ip=IPAdresse, port=Port, deviceId=deviceId, localObjName="HBS_BACNet", description="HBS BACNet Testing - by Moncef MOUZAOUI", modelName="Script by Moncef MOUZAOUI", vendorName="HBS Testing")


#

#
#binary_output(
#    instance=10,
#    name="SetState",
#    description="Output Binary",
#    presentValue=True,
#)

# Define device objects
_new_objects = analog_input(
    instance=10,
    name="Temperature",
    properties={"units": "degreesCelsius"},
    description="Input Analog",
    presentValue=10.0,
)
analog_input(
    instance=11,
    name="Humidity",
    properties={"units": "percentRelativeHumidity"},
    description="Input Analog",
    presentValue=45,
)
binary_input(
    instance=10,
    name="State",
    description="Input Binary State",
    presentValue=False,
)
binary_input(
    instance=20,
    name="Defaut",
    description="Input Binary Defaut",
    presentValue=False,
)
analog_output(
    instance=10,
    name="SetPointTemp",
    properties={"units": "degreesCelsius"},
    description="Output Analog",
    presentValue=21,
    relinquish_default=21
)

# Assign objects to device
_new_objects.add_objects_to_application(device)

eps = 0.5  # Degrees Celsius

# Main loop
print("Simulation started")
i = 0
upTMP = True
upHUM = True
while True:
    humidity = device["Humidity"].presentValue
    temperature = device["Temperature"].presentValue
    state = device["State"].presentValue
    SPtemp = device ["SetPointTemp"].presentValue
    defaut = False

    state = not state
    i+=1
    if i == 4:
        state = False
        defaut = True
        i=0
        
        
        
    if temperature > 15:
        upTMP = False
    elif temperature < 5:
        upTMP = True
    
    if humidity > 60:
        upHUM = False
    elif humidity < 40:
        upHUM = True
    
    
    if upTMP == True:
        temperature = temperature + 2
    else:
        temperature = temperature - 2
    
    if upHUM == True:
        humidity = humidity + 5
    else:
        humidity = humidity - 5
        
    
    
    
    print("state: ", state)
    print("defaut: ", defaut)
    print("temperature: ", temperature)
    print("humidity: ", humidity)
    print("SET POINT TEMPERATURE : ", SPtemp)

    # Assigning new values
    device["State"].presentValue = state
    device["Defaut"].presentValue = defaut
    device["Temperature"].presentValue = temperature
    device["Humidity"].presentValue = humidity


    # Wait for next iteration
    sleep(sleepTime)

