from Adafruit_IO import Client
import serial, time, datetime, googlemaps, pynmea2, winsound

aio_sta = Client('a79bbd0b460d40c68d98b53051e8ce12')
aio_tra = Client('b2fa5d67641a45068e3f3c7057d249dd')
gmaps = googlemaps.Client(key = 'AIzaSyCz7g7lIWptudbh68XGErWQw8ULYmE-QaU')

gps_data= serial.Serial("COM9", 9600 , timeout=0.1)
gps_data.flush()

parsed=[]
msg=0
train_arr = []
setter = 0
cbe_data = 0

def time_unit(tu):
    tu = tu.split(' ')
    return (int(tu[0].split('-')[0]))*525600 + (int(tu[0].split('-')[1]))*43800 + (int(tu[0].split('-')[2]))*1440 + (int(tu[1].split(':')[0]))*60 + int(tu[1].split(':')[1])

while True:
    setter = 0
    data = aio_sta.data('cbe')
    if (len(data) - cbe_data) != 0 :
        train_arr = []
        setter += 1

    if setter != 0:
        for i in data:
            #print time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))
            if (time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))) < 50:
                train_arr.append(int(i.value.split(",")[1]))

    i = 0
    if(gps_data.inWaiting()>0):
        data = gps_data.readline()
        if 'GPRMC' in data:
            data = data.strip('\n')
            data = data.strip('\r')
            parsed.append(data)
        for x in range(0,len(parsed)):
            msg = pynmea2.parse(parsed[x])
            if (msg.latitude != 0 or msg.longitude != 0):
                for i in train_arr:
                    loc = aio_tra.receive("trains-private-feeds." + str(i)).value.split(',')
                    loc = [float(loc[0]) , float(str(loc[1]))]
                    aio_tra.send('trains-private-feeds.16860', str(msg.latitude) + ',' + str(msg.longitude))
                    time.sleep(2)
                    dm_result = gmaps.distance_matrix((loc[0],loc[1]),(msg.latitude,msg.longitude)) 
                    #print (dm_result['rows'][0]['elements'][0]['distance']['value'])/1000.0 , i
                    if  (dm_result['rows'][0]['elements'][0]['distance']['value'])/1000.0 < 50 or (dm_result['rows'][0]['elements'][0]['duration']['value'])/60.0 < 20:
                        winsound.Beep(800,500)
                        print "Train No. " + str(i) + " is approaching. So, auto-brakes are getting applied."
      
