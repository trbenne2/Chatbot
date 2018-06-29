#Todo: [device, name device, action, field] device commands to send to server or pi

#Todo: Later on (for design day) we will add turning on and off the ac and heater

def smarthome_commands(message):
    if "lights" in message or "light" in message:                            # or u"light"
        command = light_commands(message)
        return command

    elif "temperature" in message:
        command = thermostat(message)
        return command

    else:                               # check in bot if None send None
        message.rstrip()
        command = {'message': message}
        return command


def light_commands(message):
    # {"type":0, "Action":action, "name":name}   <--- Lights JSON Action: DIM/ON/OFF Name: KITCHEN/LIVING ROOM/ALL~NULL
    # lights - dim, brigthen, on, off, increase, decrease    names for indivdual lightliving room, kitchen, all
    command = {
        'message': message,
        'type':0,
        'action': None,
        'name': None
    }

    # which light, Will update name field
    if "living room" in message:
        command['name'] = 'living room'
    elif "kitchen" in message:
        command['name'] = 'kitchen'
    else:
        command['name'] = 'all'

    # Which command, Will update action field
    if "increase" in message:
        command['action'] = 'increase'
    elif "decrease" in message:
        command['action'] = 'decrease'
    elif "brighten" in message:
        command['action'] = 'brighten'
    elif "dim" in message:
        command['action'] = 'dim'
    elif "on" in message:
        command['action'] = 'on'
    elif "off" in message:
        command['action'] = 'off'

    return command

def thermostat(message):
    # {"type": 1, "Action":action, "temp":number}   <--- thermostat JSON  action: SET/INCREASE/DECREASE temp: # degree
    # temperastat - turn on/off ac heater, increase/decrease temp by 1-10 degree, set temp to degree 50-80
    command = {
        'message': message,
        'type': 1,
        'action': None,
        'temp': None
    }

    if "change" in message or "set" in message:
        command['action'] = 'set'
        message = message.rstrip()
        tokened = message.split(' ')
        command['temp'] = tokened[-1]
    elif "increase" in message or "turn up" in message:
        command['action'] = 'increase'
        message = message.rstrip()
        tokened = message.split(' ')
        command['temp'] = tokened[-2]
    elif "decrease" in message or "turn down" in message:
        command['action'] = 'decrease'
        message = message.rstrip()
        tokened = message.split(' ')
        command['temp'] = tokened[-2]

    return command