import requests, json, pytz, re, os, time
from datetime import  timedelta, datetime
from bs4 import BeautifulSoup
from modules import calculate
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from loguru import logger
from setting import config



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

datenow = datetime.now(pytz.timezone('Europe/Berlin'))
days_ = 30
date365 = datenow + timedelta(days_)
logger.add(f'booking_error.log', format= '{time} {level} {message}', level='DEBUG', serialize=False)
path = os.path.dirname(os.path.realpath(__file__))


def  load_json(filename):
    return json.load(open(filename))

def sendToBeds24(json_data):
        url = 'https://api.beds24.com/json/setRoomDates'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain','Content-Encoding': 'utf-8'}
        send = requests.post(url, data=json.dumps(json_data), headers=headers)
        print(send.status_code)

def getListOfDates(date1='2019-01-31', date2='2019-01-31'):
    listdays = []
    start = datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.strptime(date2, '%Y-%m-%d')
    step = timedelta(days=1)
    while start <= end:
        listdays.append(start.date())
        start += step
    return listdays


# new line
def getListOfDates2(date1='2019-01-31', date2='2019-01-31'):
    listdays = []
    start = datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.strptime(date2, '%Y-%m-%d')
    step = timedelta(days=1)
    while start <= end:
        listdays.append(start.date().strftime('%Y-%m-%d'))
        start += step
    return listdays


def parsing_hotels(checkin = '2020-04-30', checkout= '2020-05-01'):
    hotels_price = []

    data_json = load_json(f'{path}/config/listofhotels.json')
    
    for url in data_json:
        link = f'{url["url"]}checkin={checkin};checkout={checkout};dist=0;group_adults=1;group_children=0;no_rooms=1;sb_price_type=total;sr_order=popularity;type=total;selected_currency=EUR;'
        hotel_data = requests.get(link, headers=headers)
        soup = BeautifulSoup(hotel_data.content, 'lxml')
        hotel_name = url['full_name']
        try:
            hotel_price = soup.select('span.prco-valign-middle-helper')[0].text.strip()
            hotel_price = int(''.join(re.findall('[0-9]+', hotel_price)))
        except:
            hotel_price = 0
        print(hotel_name, hotel_price)
        hotels_price.append({'hotel_name': hotel_name, 
                             'hotel_price': hotel_price})
    return hotels_price

@logger.catch
def getRooms(d1, d2):
    params = {'authentication': {'apiKey':config('API_KEY'), 'propKey':config('PROP_KEY')},'roomId':'154156','from':d1.strftime('%Y%m%d'),'to':d2.strftime('%Y%m%d')}
    data = requests.post('https://api.beds24.com/json/getRoomDates', data = json.dumps(params))
    list_days = getListOfDates(d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'))
    days = 1
    data_json = load_json(f'{path}/config/hotel.json')
    
    booking_data = []
    for i in list_days:
        xls_data = {}
        booking_price = []
        room = data.json()[str(i.strftime('%Y%m%d'))]['i']
        prices = parsing_hotels(str(i), str(i + timedelta(1)))

        for p in prices:
            booking_price.append(p["hotel_price"])
        calc = calculate.Calculate(booking_price)
        n_price = int(calc.newPrice(room, days, calc.rate(calc.min(),calc.mid()), calc.min(), calc.mid(), calc.SoldOutRate(), calc.max()))
        print (days, i.strftime('%Y-%m-%d'), '---------------------', n_price)
        if i.strftime('%Y-%m-%d') in getListOfDates2(calc.setting2[0], calc.setting2[1]) and days >= calc.setting2[3]:
            n_price = n_price * float(calc.setting2[2])
            print (n_price, f'this is mult on {float(calc.setting2[2])} setting2', i.strftime('%Y-%m-%d'))
        elif i.strftime('%Y-%m-%d') in getListOfDates2(calc.setting[0], calc.setting[1]) and days >= calc.setting[3]:
            n_price = n_price * float(calc.setting[2])
            print (n_price, f'this is mult on {float(calc.setting[2])} setting1', i.strftime('%Y-%m-%d'))
        von = i.strftime('%d-%m-%Y')
        bis = (i + timedelta(1)).strftime('%d-%m-%Y')
        xls_data.update({'Von': von})
        xls_data.update({'Bis': bis})
        xls_data.update({'days': days})
        xls_data.update({'room': room})
        xls_data.update({'rate': round(calc.rate(calc.min(),calc.mid()),1)})
        xls_data.update({'mid': int(calc.mid())})
        xls_data.update({'min': calc.min()})
        xls_data.update({'market': round(calc.SoldOutRate(),1)})
        xls_data.update({'my price': int(n_price)})
        for p in prices:
            xls_data.update({p["hotel_name"] : p["hotel_price"]})
        
        booking_data.append(xls_data)
        data_json['dates'][i.strftime('%Y%m%d')] = {'p1': str(n_price)}
        days +=1
        
    return booking_data, data_json

def send_email():
    USER = config('USER_MAIL')
    KEY = config('KEY_MAIL')
    msg = MIMEMultipart('USER')
    msg['Subject'] = 'booking price' 
    msg['From'] = config('FROM')
    msg['To'] = config('FROM')
    adresses = ['myroomtopapartment@gmail.com', 'j@grobman.de', 'alxgav@gmail.com']
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(f'{path}/out/booking.xlsx', "rb").read())
    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="booking.xlsx"')

    msg.attach(part)
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(USER, KEY)
  
    server.sendmail(msg['From'], adresses, msg.as_string())
    server.quit() 
    print('message send', adresses)


def write_to_excel(df, filename):
    num_of_column = len(df.columns)
    writer = pd.ExcelWriter(filename)
    sheet_name = 'booking'
    # df.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='NaN')
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    worksheet.set_default_row(hide_unused_rows=True)
    # merge_format = workbook.add_format({'align': 'left', 'valign': 'vcenter'})
    center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    header_format = workbook.add_format({'bold': True,
                                        'fg_color': '#D4D3D3',
                                        'border': 1, 'text_wrap': True,
                                        'align': 'center', 'valign': 'vcenter'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.set_row(0, 25)
        worksheet.write(0, col_num, value, header_format) 
                                           
    for col in range(9):
        writer.sheets[sheet_name].set_column(col, col, 10, center_format)
    for col in range(9, num_of_column):
        writer.sheets[sheet_name].set_column(col, col, 30, center_format)
    worksheet.set_default_row(15)
    

    writer.save()
if __name__ == "__main__":
    data, data_json = getRooms(datenow, date365)
    df = pd.DataFrame(data)
    df = df[['Von',
             'Bis', 
             'days','room', 'rate', 'mid', 'min', 'market',  'my price',
             'H2 Hotel München Messe', 
             'H4 Hotel München Messe', 
             'Motel One München-Messe', 
             'Premium Apartment München Messe']]
    write_to_excel(df, f'{path}/out/booking.xlsx')
    # sendToBeds24(data_json)
    # send_email()
   
