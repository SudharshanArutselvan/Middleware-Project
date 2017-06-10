from pubnub import Pubnub
import json

pubnub = Pubnub(publish_key = 'pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac', subscribe_key = 'sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f')

DeviceStatus = False
DeviceName = {}
SendStatus = {}

#Publish Channels
GetDeviceChannel = "GetDevices"
RetrieveStatusChannel = "RetrieveStatus"

#Subscribe Channels
StatusReportChannel = "StatusReport"
IndividualChannel = "Room1Light1"
room = "Room1"
device = "Light1"

def Initialization():
    global DeviceName
    global SendStatus
    global DeviceStatus
    global IndividualChannel
    global room
    global device
    
    DeviceName={"Actuators":{
                    room:{
                        device:{
                            "Status":DeviceStatus,"Channel":IndividualChannel
                        }
                    }
                }
                };

    SendStatus={"Actuators":{
                    room:{
                        device:DeviceStatus
                    }
                }
                };
    #Give Intro
    pubnub.publish(channel = GetDeviceChannel, message = DeviceName)



def DeviceControlCallback(message,channel):
    global DeviceStatus
    print message
    split = message.split(":");
    if(split[0]=="false"):
        DeviceStatus = False
    else:
        DeviceStatus = True

def StatusReportCallback(message,channel):
    global SendStatus
    SendStatus={"Actuators":{
                    room:{
                        device:DeviceStatus
                    }
                }
                };
    pubnub.publish(channel = RetrieveStatusChannel, message = SendStatus)

Initialization()
pubnub.subscribe( IndividualChannel, callback = DeviceControlCallback)
pubnub.subscribe( StatusReportChannel, callback = StatusReportCallback)


