from Adafruit_IO import Client, Feed
import datetime

aio_sta = Client('**************************') #In place of * paste your AIO key
pgt_len = tup_len = 0
train_arr = []

def time_unit(tu):
    tu = tu.split(' ')
    return (int(tu[0].split('-')[0]))*525600 + (int(tu[0].split('-')[1]))*43800 + (int(tu[0].split('-')[2]))*1440 + (int(tu[1].split(':')[0]))*60 + int(tu[1].split(':')[1])

while True:
    setter = 0
    pgt = aio_sta.data('station-particular-feeds.pgt')
    if (len(pgt) - pgt_len) != 0 :
        aio_sta.delete_feed('cbe')
        aio_sta.create_feed(Feed(name='CBE'))
        setter += 1
    pgt_len = len(pgt)
    
    tup = aio_sta.data('station-particular-feeds.tup')
    if (len(tup) - tup_len) != 0 :
        aio_sta.delete_feed('cbe')
        aio_sta.create_feed(Feed(name='CBE'))
        setter += 1
    tup_len = len(tup)

    if setter != 0:
        for i in pgt:
            print time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))
            if (time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))) < 50:
                aio_sta.send('cbe', str(i.value))

        i = 0
        for i in tup:
            if (time_unit(str(datetime.datetime.now())) -  time_unit(str(i.value.split(",")[0]))) < 50:
                aio_sta.send('cbe', str(i.value))
