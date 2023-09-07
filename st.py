import requests, json

from pprint import pprint
from datetime import  timedelta, datetime
import pandas as pd
from modules import mailto


zimmer = {"1":"151", "2":"148", '3':'6', '4':'7', '5': '134', '6':'138', '7':'139', '8':'29', '9':'30' }

# d_t = datetime.today() - timedelta(days=2)
d_t = datetime.strptime('2021-07-10', '%Y-%m-%d')

firstday = d_t.replace(day=1)
lastday = (d_t.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

def getSt():
    DATA_JSON = {"authentication": {"apiKey":"testtesttesttesttest", "propKey":"66197apitest66197apitest"},"roomId":"154156", "arrivalFrom": "20100101"}
    data = requests.post('https://www.beds24.com/api/json/getBookings', data = json.dumps(DATA_JSON))
    # f = open('data.json', 'w')
    # json.dump(data.json(), f,  indent=4)
    return data

def readTestData(filename = 'data.json'):
    f = open(filename, 'r')
    return json.load(f)


def getRoomNumber(unitId):
    room = '0'
    for k, v in zimmer.items():
        if unitId == k:
            room = v
    return room

def getDays(d1, d2):
    start = datetime.strptime(d1, '%Y-%m-%d')
    end = datetime.strptime(d2, '%Y-%m-%d')
    d = end - start
    return d.days
    

def getListOfDates(date1='2019-07-01', date2='2019-07-10'):
    listdays = []
    start = datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.strptime(date2, '%Y-%m-%d')
    step = timedelta(days=1)
    while start <= end:
        listdays.append(start.date().strftime('%Y-%m-%d'))
        start += step
    return listdays



def getListOfMonth(date1='2019-07-01', date2='2019-07-10'):
    listdays = []
    start = datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.strptime(date2, '%Y-%m-%d')
    step = timedelta(days=1)
    while start <= end:
        listdays.append(start.date().strftime('%Y%m'))
        start += step
    new_list = []
    for i in listdays:
        if i not in new_list:
            new_list.append(i)
    return new_list




def getListOfTheMonth():
    return getListOfDates(firstday.strftime('%Y-%m-%d'), lastday.strftime('%Y-%m-%d'))

def getDaysOfMonth():
    return getDays(firstday.strftime('%Y-%m-%d'), lastday.strftime('%Y-%m-%d')) + 1



def getStatus(data):
    room_data = []
    month = d_t.strftime('%Y%m')
    day_m = getDaysOfMonth()
    # test data
    # month = '202106'
    # firstday = datetime.strptime('2021-06-01', '%Y-%m-%d')
    # lastday = datetime.strptime('2021-06-30', '%Y-%m-%d')
    # day_m = 30
    # end test data
    
    for i in data.json(): #after test uncomment
    # for i in data: # delete sfter test
        status = int(i["status"])
        room_number = int(getRoomNumber(i["unitId"]))
        
        days = int(getDays(i["firstNight"], i["lastNight"]))
        if days == 0:
            days = 1
        if status == 4 and room_number !=0:
            if month in getListOfMonth(i["firstNight"], i["lastNight"]):
                d_f = datetime.strptime(i["firstNight"], '%Y-%m-%d') -  firstday
                d_l = lastday - datetime.strptime(i["lastNight"], '%Y-%m-%d')
                roomDays = []
                for d in getListOfDates(i["firstNight"], i["lastNight"]):
                    if d[5:7] == '06':
                        roomDays.append('')
                # print (d_f.days, d_l.days, room_number, len(roomDays), day_m)
                
                room_data.append({'room_number': room_number,
                                      'bookid': i["bookId"],
                                      'firstNigth': i["firstNight"],
                                      'lastNigth':i["lastNight"],
                                      'days': days,
                                      'days_month':len(roomDays),
                                      'status': status,
                                      'persent': round(len(roomDays)/day_m,2),
                             })
                    
    return room_data




if __name__ == "__main__":
    # pprint(readTestData())
    # data = getStatus(readTestData())
    SUBJECT = f'Black not Black for {d_t.strftime("%B")}'
    FROM = 'alxgav@gmail.com'
    addresses = ['alxgav@yandex.ru', 'j@grobman.de']
    data = getStatus(getSt())
    black = []
    rooms = {}
    
    for i in data:
        black.append(i['persent'])
            
    black_all = sum(black)
    not_black = round((9 - black_all), 2)

    rooms.update({'black long term':[black_all, f'{int((black_all/9)*100)}% '], 
                  'not black short term': [not_black,f'{int((not_black/9)*100)}% ']})


    df = pd.DataFrame(rooms)
    table = df.to_html()  

    

    mailto.send_email(SUBJECT, FROM, addresses, table)
    print(SUBJECT)

   
