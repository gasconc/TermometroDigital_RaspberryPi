#!/usr/bin/python
import sys
import Adafruit_DHT
import time
from datetime import datetime
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Creacion e Inicializacion de Objeto tipo pantallita LCD 
# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Inicializando Display.
disp.begin(contrast=60)

#Limpiando display.
disp.clear()
disp.display()

#Nueva Imagen
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

#creacion del objeto draw 
draw = ImageDraw.Draw(image)

#Creacion de un rectangulo vacio de la misma dimension del display.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

#Cargando el tipo de fuente por defecto
font = ImageFont.load_default()

#Analisis de parametros de la Terminal
sensor_args = { '11': Adafruit_DHT.DHT11,
				'22': Adafruit_DHT.DHT22,
				'2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
	sensor = sensor_args[sys.argv[1]]
	pin = sys.argv[2]
else:
	print 'usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#'
	print 'example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4'
	sys.exit(1)



#Conversion de centigrados a grados Farenheit
# temperature = temperature * 9/5.0 + 32

while 1 == 1:
	
	#Comunicacion con el sensor por medio del metodo read_retry
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	  
	#Validando que la lectura no sea Null.
	if humidity is not None and temperature is not None:
		#Escritura del texto
		draw.rectangle((0,0,83,47), outline=255, fill=255)
		draw.text((1,1),datetime.now().strftime('%b %d'), font=font)
		draw.text((1,10),datetime.now().strftime('%I:%M:%S %p'), font=font)
		print('Temp = {0:0.1f}*'.format(temperature, humidity))
		draw.text((1,20),'Temp = {0:0.1f}*'.format(temperature, humidity), font=font)
		draw.text((1,30),'RH% = {1:0.1f}%'.format(temperature, humidity), font=font)
		#disp.clear()
	else:
		draw.text((1,20),'Medicion Fallida', font=font)

	#Mostrar la imagen.
	disp.image(image)
	disp.display()


