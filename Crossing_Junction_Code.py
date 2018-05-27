from Adafruit_IO import Client
import datetime, googlemaps , winsound

aio_sta = Client('**************************') #In place of * paste your AIO key
aio_tra = Client('**************************') #In place of * paste your AIO key
gmaps = googlemaps.Client(key = '**********************') #In place of * paste your Google API key
cbe_len = pgt_len = 0
train_arr = []

def time_unit(tu):
    tu = tu.split(' ')
    return (int(tu[0].split('-')[0]))*525600 + (int(tu[0].split('-')[1]))*43800 + (int(tu[0].split('-')[2]))*1440 + (int(tu[1].split(':')[0]))*60 + int(tu[1].split(':')[1])
    
## For the crossing station
while True:
    setter = 0
    cbe = aio_sta.data('station-particular-feeds.cbe')
    if (len(cbe) - cbe_len) != 0 :
        train_arr = []
        setter += 1
    cbe_len = len(cbe)
    
    pgt = aio_sta.data('station-particular-feeds.pgt')
    if (len(pgt) - pgt_len) != 0 :
        train_arr = []
        setter += 1
    pgt_len = len(pgt)

    if setter != 0:
        for i in cbe:
            #temp = int((i.value.split(",")[0].split(' ')[1].split(':')[0]))*60 + int(i.value.split(",")[0].split(' ')[1].split(':')[1])
            #print temp - ((datetime.datetime.now().hour)*60 + datetime.datetime.now().minute)
            if (time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))) < 45:
                train_arr.append(int(i.value.split(",")[1]))

        i = 0
        for i in pgt:
            #temp = int((i.value.split(",")[0].split(' ')[1].split(':')[0]))*60 + int(i.value.split(",")[0].split(' ')[1].split(':')[1])
            #print time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))
            if (time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))) < 45:
                train_arr.append(int(i.value.split(",")[1]))
            
    print train_arr 

    i = 0
    for i in train_arr:
        loc = aio_tra.receive("trains-private-feeds." + str(i)).value.split(',')
        loc = [float(loc[0]) , float(str(loc[1]))]
        dm_result = gmaps.distance_matrix((loc[0],loc[1]),(17.5333,78.5153)) #These are the static co-ordinates of the crossing junction.
        
        if  (dm_result['rows'][0]['elements'][0]['distance']['value'])/1000.0 < 40 or (dm_result['rows'][0]['elements'][0]['duration']['value'])/60.0 < 0:
            winsound.Beep(800,500)
            print "Train No. " + str(i) + " is approaching. So, gates are getting closed please move away..!!"
            
        
        
