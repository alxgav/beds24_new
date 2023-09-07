#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import division
from datetime import datetime

class Calculate:
  
    setting = ['2020-10-08', '2020-10-10', 6, 1, 85] # ментять при необходимости
    setting2 = ['2020-09-07', '2020-09-12', 6, 1, 200] # ментять при необходимости
    setting3 = [{'2020-10-14':70,
                 '2020-10-15':85,
                 '2020-10-16':70,
                 '2020-10-17':65}] #тут можно добавлять даты с ценой
    
    def __init__(self, prices):
        self.prices = prices

    def min(self):
        if sum(self.prices)>0:
            return min(list(filter(lambda a: a != 0, self.prices))) 
        else:
            return 0    

    def max(self):
        return max(self.prices)
    
    def mid(self):
        size = len(list(filter(lambda a: a != 0, self.prices)))
        if size != 0:
            return sum(self.prices)/size	
        else:
            return 500 

    def rate(self, min, mid):
        if min > 0:
            return min/mid
        else:
            return 0 

    def newPrice(self, room, daysnow, rate, min, mid, market, max):
        price = 800
        d = datetime.today()
        t = int(d.strftime('%H'))
        
        if daysnow > 14:
            price = 600
        if price == 0:
            return 600
        if daysnow <= 3:
            price=min-2
        if daysnow <= 31 and daysnow > 7 and room > 2:
            price = (mid+min)/2
        if daysnow <= 14 and daysnow > 7:
            price = min-2+(mid-min)/4*(10-room)	
        if market > 0.7 and mid < 95:
            price = min-2
        if market < 0.3:
            price = 600   
        if daysnow <= 7 and daysnow > 3 and room <= 2:
            price = (mid+min)/2
        if daysnow <= 7 and daysnow > 3 and room <= 2 and min > 100:
            price = min-2+(mid-min)/4*(10-room)
        if daysnow <= 14 and daysnow > 3 and market < 0.5 and market > 0 and mid > 95:
            price = (mid+min)/2   
        if daysnow <= 7 and daysnow > 3 and room > 2:
            price = (mid+min)/2
        if daysnow <= 7 and daysnow > 2 and room >= 2 and mid < 200 and rate > 0.6:
            price = min-2
        if daysnow <= 7 and daysnow > 2 and room > 2 and rate >= 0.6:
            price = min-2
        if daysnow <= 7 and daysnow > 3 and room > 2 and rate < 0.5:
            price = (mid+min)/2
        if daysnow > 3 and room > 2 and rate < 0.6:
            price = (mid+min)/2
        if room > 2 and min > 200 and rate > 0.7:
            price = min-2
        if room > 2 and min > 200 and rate <= 0.7:
            price = (mid+min)/2
        if daysnow <= 3 and market < 0.3 and room <= 2:
            price = 100
        if daysnow <= 31 and daysnow > 7 and market > 0.3 and room <= 2:
            price = (mid+min)/2
        if daysnow <= 7 and daysnow > 3 and market < 0.3 and market > 0 and room <= 3:
            price = (mid+min)/2
        if daysnow <= 31 and daysnow > 3 and room >= 1 and market > 0.7 and mid < 95 and rate >= 0.8:
            price = min-2
        if daysnow <= 31 and daysnow > 14 and market < 0.5 and market > 0.1 and mid >100:
            price = (mid+min)/2
        if daysnow <= 31 and daysnow > 14 and market < 0.5 and market > 0.1 and mid <100:
            price = min-2+(mid-min)/4*(10-room)
        if daysnow <= 31 and daysnow > 14 and market > 0.5 and mid > 95:
            price = (mid+min)/2
        if daysnow <= 19 and daysnow > 14 and market < 0.1:
            price = 300-room*15
        if daysnow <= 24 and daysnow > 19 and market < 0.1:
            price = 400-room*15
        if daysnow <= 31 and daysnow > 24 and market < 0.1:
            price = 500-room*15
        if daysnow <= 14 and daysnow > 7 and market < 0.3:
            price = 300-room*15
        if daysnow <= 14 and daysnow > 7 and market > 0 and market < 0.3:
            price = (mid+min)/2			
        if daysnow <= 7 and daysnow > 3 and market == 0:
            price = 70+(10-room)*15			
        if daysnow <= 31 and daysnow > 3 and room >= 2 and market > 0.7 and mid < 80 and min < 66 and rate >= 0.8:
            price = 60
        if daysnow <= 14 and daysnow > 3 and market > 0 and rate > 0.7 and room <= 3 and min > 300:
            price = min-2    
        if daysnow <= 7 and daysnow > 3 and market > 0 and min > 300:
            price = min*0.9
        if daysnow >= 7 and price > 1000 and mid > 2000:
            price = 400
        if daysnow <= 14 and daysnow > 1 and mid >200:
            price = (100+10*(10-room))*(-1/daysnow+1)
        if daysnow <= 14 and daysnow > 1 and mid >250:
            price = (150+10*(10-room))*(-1/daysnow+1)
        if daysnow <= 14 and daysnow > 1 and mid >300:
            price = (150+10*(10-room))*(-1/daysnow+1)
        if daysnow <= 14 and daysnow > 1 and mid >350:
            price = (200+10*(10-room))*(-1/daysnow+1)
        if daysnow <= 14 and daysnow > 1 and mid >400:
            price = (300+15*(10-room))*(-1/daysnow+1)
        #if room == 0:
        #    price = 1000
        #if daysnow <= 30:
        #    price = Q2-((Q2-(R2+((R2+(Q2-R2)*(1-(D2/10)))-R2)*C2/30))*(1-(C2/30)))
        #if daysnow == 1 and room > 0 and time.strftime('%H')>12:
        #    price = 60
        #if daysnow == 1 and room > 0 and time.strftime('%H')>1:
        #    price = min * 0.7
        #if price < 60 and daysnow > 1:
        #    price = 60+(10-room)*3            
        if daysnow < 30 and d.weekday() >= 5 and price < 60:
            print ('new if =============================================== new if')
            price = 60
        if room > 0 and daysnow <= 31:
            price = max-((max-(min+((min+(max-min)*(1-(room/10)))-min)*market))*(1-(daysnow/30)))
        #if daysnow <= 30:
        #    price = ((MIN+(MAX-MIN)*daysnow/30)+(MIN+(MAX-MIN)*(1-(room/10)))+(MAX-(MAX-MIN)*market))/3
        if room > 0 and daysnow <= 31:
            price = mid-((mid-(min+((min+(mid-min)*(1-(room/10)))-min)*market))*(1-(daysnow/30)))
        if d.weekday() < 5 and price < 60 and daysnow < 4:
            price = 60
        if d.weekday() < 5 and price < 60 and daysnow > 3:
            price = 60
        if daysnow <= 3 and room > 0:
            price = min*0.8    
        if daysnow <= 3 and room > 0 and market == 0:
            price = 90+(10-room)*10	 
        if daysnow <= 2 and room > 0:
            price = min*0.6    
        if daysnow <= 2 and room > 0 and market == 0:
            price = 80+(10-room)*5
        if daysnow <= 2 and room <=2 and market <= 0.6:
            price = min*0.8   
        if daysnow == 1 and room > 0 and min > 70:
            price = 70
        if daysnow == 1 and room > 0 and min <= 70:
            price = min-2
        if daysnow == 1 and room > 0 and market == 0:
            price = 60+(10-room)*5
        if daysnow == 1 and room > 0 and min > 100:
            price = min*0.8
        if daysnow < 7 and price > 1000 and mid > 2000:
            price = min-2
        if daysnow == 1 and room > 0 and t > 12:
            print (t, 'min price after 18')
            price = 60
        if daysnow == 1 and room > 0 and t > 15:
            print (t, 'min price after 18')
            price = 60
        if daysnow == 1 and room > 0 and t > 18:
            print (t, 'min price after 18')
            price = 60
        if price < 79: 
            price = 70
        return price   

    def SoldOutRate(self): #market
        room_size = len(self.prices)
        room_size_zero = len(list(filter(lambda a: a!=0, self.prices)))
        return room_size_zero/room_size
