import serial
import string
import socket
import os


def main():
    ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
    try:
        ser.open()
    except Exception:
        raise
    while True:
        dataToWrite = ser.readline()
        with open (gpsdata.txt, 'a') as f: f.write (dataToWrite + '\n')

main()