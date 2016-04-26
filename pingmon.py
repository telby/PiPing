import time
import serial
import string
import socket
import os
import io
import datetime
import ftplib
import logging
from pynmea import nmea

def location():
    ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=1)
    try:
        ser.open()
    except Exception:
        logging.exception('Could not open serial connection')
        raise
    ser.flushInput()
    ser.flushOutput()
    gpgga = nmea.GPGGA()
    while True:
        try:
            data = ser.readline()
        except Exception:
            logging.exception('Could not read from serial connection')
            print ('could not read from serial connection')
            raise
        try:
            dataDecoded = bytes.decode(data)
        except UnicodeDecodeError:
            dataDecoded = "null"
            logging.exception('Unicode decode failed')
            pass
        except Exception:
            logging.exception('Error decoding serial buffer')
            raise
        if dataDecoded[0:6] == '$GPGGA':
            gpgga.parse(dataDecoded)
            lat = gpgga.latitude
            if not lat:
                logging.warning('No GPS fix')
                gps_time = gpgga.timestamp
                latlontim = "0"
                return (latlontim)
            else:
                lat_dir = gpgga.lat_direction
                lon = gpgga.longitude
                lon_dir = gpgga.lon_direction
                time_stamp = gpgga.timestamp
                alt = gpgga.antenna_altitude
                lat_deg = float(lat[0:2])
                lat_min = float(lat[2:4])/60
                lat_secs = float(lat[5:])*60/10000
                lat_secs = lat_secs/3600
                latitude = lat_deg + lat_min + lat_secs
                lon_deg = float(lon[0:3])
                lon_min = float(lon[3:5])/60
                lon_secs = float(lon[6:])*60/10000
                lon_secs = lon_secs/3600
                longitude = (lon_deg + lon_min + lon_secs)*-1
                gps_time = gpgga.timestamp
                lat = None
                lon = None
                latlontim = str(latitude) + ',' + str(longitude) + ',' + str(gps_time)
                return (latlontim)

def main ():
    logging.basicConfig(filename='error.log', format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
    id = 'Test-pi'
    hostname = '8.8.8.8'
    pingFailCount = 0
    pingSuccessCount = 0
    logName = 'piPingLog.txt'
    ftpFail = 0

    while True:
        time.sleep(1)
        response = os.system("ping -c 1 " + hostname)
        print ('ping')
        if response == 0:
            pingSuccessCount = pingSuccessCount + 1
            print (pingSuccessCount)
            pingFailCount = 0
            if pingSuccessCount >= 20:
                try:
                    session = ftplib.FTP('','','')
                    with open(logName, 'rb') as file:
                        session.storbinary('APPE piPingLog.txt', file)
                        session.quit
                    ftpFail = 0
                    logging.info('FTP upload error')
                except ftplib.all_errors:
                    logging.exception('FTP upload error')
                    ftpFail = 1
                    raise
                except Exception:
                    logging.exception('Error writing and uploading file to FTP')
                    ftpFail = 1
                    raise
                pingSuccessCount = 0
                if ftpFail == 0:
                    f = open('masterpi.txt', 'a')
                    with open(logName, 'r') as a:
                        for line in a:
                            f.write(line)
                    f.close()
                    a.close()
                    open(logName, 'w').close()
            pass
        else:
            pingFailCount = pingFailCount + 1
            pingSuccessCount = 0
            gpsLocation = location()
            if gpsLocation != "0"
                output = id + ','  + hostname + ',' + str(pingFailCount) + ',' + gpsLocation + ',' + str(datetime.datetime.now())
                with open (logName, 'a') as f: f.write(output + '\n')
                print (output)
            else
                pass
    return(0)


main()

