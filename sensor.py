from sense_hat import SenseHat

sense =  SenseHat()
fmt = "Humidity: {0:.1f}%,Temp: {1:.1f}C,Pressure: {2:.1f}Mb"

hum = sense.get_humidity()
press = sense.get_pressure()
temp = sense.get_temperature_from_pressure()
sense.set_rotation(180)
print(fmt.format(hum,temp,press))
sense.show_message(fmt.format(hum,temp,press))
