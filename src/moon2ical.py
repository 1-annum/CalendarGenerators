#!/usr/bin/env python
"""
moonphase.py - Calculate Lunar Phase
Author: Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
"""

import math, decimal, datetime
import uuid

dec = decimal.Decimal

ical_openings="""BEGIN:VCALENDAR
VERSION:2.0
PRODID:1-annum
"""

first_quarter_ical_str="""BEGIN:VEVENT
UID:%s@1-annum.com
CATEGORIES:MOON
DTSTAMP:20201231T103500Z
TRANSP:TRANSPARENT
LAST-MODIFIED:20201231T103500Z
STATUS:CONFIRMED
DTSTART:%s
DTEND:%s
SUMMARY:Moon - First Quarter
END:VEVENT
"""
last_quarter_ical_str="""BEGIN:VEVENT
UID:%s@1-annum.com
CATEGORIES:MOON
DTSTAMP:20201231T103500Z
TRANSP:TRANSPARENT
LAST-MODIFIED:20201231T103500Z
STATUS:CONFIRMED
DTSTART:%s
DTEND:%s
SUMMARY:Moon - Last Quarter
END:VEVENT
"""
full_moon_ical_str="""BEGIN:VEVENT
UID:%s@1-annum.com
CATEGORIES:MOON
DTSTAMP:20201231T103500Z
TRANSP:TRANSPARENT
LAST-MODIFIED:20201231T103500Z
STATUS:CONFIRMED
DTSTART:%s
DTEND:%s
SUMMARY:Moon - Full Moon
END:VEVENT
"""
new_moon_ical_str="""BEGIN:VEVENT
UID:%s@1-annum.com
CATEGORIES:MOON
DTSTAMP:20201231T103500Z
TRANSP:TRANSPARENT
LAST-MODIFIED:20201231T103500Z
STATUS:CONFIRMED
DTSTART:%s
DTEND:%s
SUMMARY:Moon - New Moon
END:VEVENT
"""


def position(now=None): 
   if now is None: 
      now = datetime.datetime.now()

   diff = now - datetime.datetime(2001, 1, 1)
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   return lunations % dec(1)

def phase(pos): 
   index = (pos * dec(8)) + dec("0.5")
   index = math.floor(index)
   return {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }[int(index) & 7]

def get_list_phases(year_start=2001,year_end=2030):
    delta_start = (datetime.date(year_start,1,1)-datetime.date(2001,1,1)).days
    delta_end = (datetime.date(year_end,12,31)-datetime.date(2001,1,1)).days 
    print(38,delta_start,delta_end)
    last_year_date = datetime.datetime(2001,1,1)+datetime.timedelta(days=delta_start-1)
    pos=position(last_year_date)
    prev = round(float(pos), 3)
    list_days = []
    for days_offset in range(delta_start,delta_end): #day_count+1):
        date_query=datetime.datetime(2001,1,1)+datetime.timedelta(days=days_offset)
        pos = position(date_query)
        phasename=phase(pos)
        roundedpos = round(float(pos), 3)
        if roundedpos<0.05 and prev>0.95:
            #new moon
            if abs(prev-1)>abs(roundedpos):
                date_query = prev_date
            list_days.append((date_query,"New Moon"))
                
        elif roundedpos>0.75 and prev<0.75:
            #last quarter
            if abs(prev-0.75)<abs(roundedpos-0.75):
                date_query = prev_date
            list_days.append((date_query,"Last Quarter"))
        elif roundedpos>0.25 and prev<0.25:
            #first quarter
            if abs(prev-0.25)<abs(roundedpos-0.25):
                date_query = prev_date
            list_days.append((date_query,"First Quarter"))
        elif roundedpos>0.5 and prev<0.5:
            #full moon
            if abs(prev-0.5)<abs(roundedpos-0.5):
                date_query = prev_date
            list_days.append((date_query,"Full Moon"))
        prev = roundedpos
        prev_date = date_query
            
    #print("%s %s (%s)" % (date_query, phasename, roundedpos))
    return list_days
    
def make_ical(year_start=2000,year_end=2040):
    list_days = get_list_phases(year_start,year_end)
    with open("moon_%s_%s.ics"%(year_start,year_end),"w") as fo:
        fo.write(ical_openings)
        for day in list_days:
            event_uuid = str(uuid.uuid4())
            dts = day[0].strftime("%Y%m%dT%H%m%SZ")
            dte = day[0].strftime("%Y%m%dT%H%m%SZ") 
            if day[1]=="First Quarter":
                fo.write(first_quarter_ical_str%(event_uuid,dts,dte))
            elif day[1]=="Last Quarter":
                fo.write(last_quarter_ical_str%(event_uuid,dts,dte))
            elif day[1]=="New Moon":
                fo.write(new_moon_ical_str%(event_uuid,dts,dte))
            elif day[1]=="Full Moon":
                fo.write(full_moon_ical_str%(event_uuid,dts,dte))
        fo.write("END:VCALENDAR")
    

def main(): 
   pos = position()
   phasename = phase(pos)

   roundedpos = round(float(pos), 3)
   print("%s (%s)" % (phasename, roundedpos))

if __name__=="__main__": 
   make_ical()