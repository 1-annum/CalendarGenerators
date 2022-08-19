""" Make Germany / Bavaria public holiday by leveraging
moving catholic moving feast generator
"""

import holidays
import itertools
from datetime import date
import uuid

from MakeiCal import write_ical

"""
cal_header="" "BEGIN:VCALENDAR
VERSION:2.0
METHOD:PUBLISH
PRODID:1-annum
"" "

cal_footer="END:VCALENDAR"

def yearly_recur_ics(dstart,uid,summary):
    vevent="" "BEGIN:VEVENT
DTSTART;VALUE=DATE:%s
DTEND;VALUE=DATE:%s
RRULE:FREQ=YEARLY;
UID:%s
DTSTAMP:19970714T170000Z
ORGANIZER;CN=Auberon Vacher:MAILTO:contact@1-annum.com
SUMMARY: %s 
END:VEVENT
"" "
    dstart=dstart.strftime("%Y%m%dT%H%m%SZ")
    return vevent%(dstart,dstart,uid,summary)
    
def non_recur(dates,uid,summary,):
    vevent="" "BEGIN:VEVENT
DTSTART;VALUE=DATE:%s
DTEND;VALUE=DATE:%s
RDATE;VALUE=DATE:%s
UID:%s
DTSTAMP:19970714T170000Z
ORGANIZER;CN=Auberon Vacher:MAILTO:contact@1-annum.com
SUMMARY: %s 
END:VEVENT
"" "
    def mygrouper(n, iterable):
        args = [iter(iterable)] * n
        return ([e for e in t if e != None] for t in itertools.zip_longest(*args))
    
    dates = [d.strftime("%Y%m%dT%H%m%SZ") for d in dates]
    dts = dates[0]
    dte = dates[0]
    #TODO: since ical lines must be <75 characters - splitting every 4 dates
    dates = list(mygrouper(3,dates))
    str_dates = []
    for d in dates:
        str_dates.append(",".join(d))
    dates="\n ".join(str_dates)
    return vevent%(dts,dte,dates,uid,summary,)
"""

def make_country_holiday(iso,start=2000,end=2040):
    #dates is 
    dates={}
    fixed={}
    moving={}
    events={}
    lang="iso"
    #for date, name in sorted(holidays.DE(prov="BY",years=[2020]).items()):
    #    dates[name]=date
    
    #first go over all the events as we do not know yet:
    # if they recur
    # if they recur do they haver yearly recurence or not
    # non-yearly recurrning will be saved in ical as RDATE
    years_range = range(start,end)
    holidays_countries = {"FR":holidays.FR(years=years_range).items,
                          "GB":holidays.GB(years=years_range).items,
                          "DE":holidays.DE(prov="BY",years=years_range).items,
                          "JP":holidays.JP(years=years_range).items
                            }
    for date, names in sorted(holidays_countries[iso]()):
        #names can be comma separated when multiple holiday happen on the same day
        for name in names.split(", "):
            if name in events:
                events[name]["dates"].append(date)
            else:
                events[name]={"dates":[date],lang:name}
    moving=events.copy()
    
    rdates = {}
    rrules = {}
    
    for event in events:
        rrule=True
        for date in events[event]["dates"]:
            if not ( date.month==events[event]["dates"][0].month and \
                     date.day==events[event]["dates"][0].day and \
                     len(events[event]["dates"])==len(years_range)):
                rrule=False
        if rrule:
            rrules[event.replace("(Observed)","")]={"dtstart":events[event]["dates"][0],"rrule":"FREQ=YEARLY;"}
            del moving[event]
        else:
            rdates[event.replace("(Observed)","")]=events[event]["dates"]
    
    write_ical("%s_ferie_%s_%s.ics"%(iso,start,end),rrules,rdates)
    """
    with open("%s_ferie_%s_%s.ics"%(iso,start,end),"w",encoding='utf-8') as fo:
        fo.write(cal_header)
        for ferien in fixed:
            print("fixed",ferien)
            event_uuid = str(uuid.uuid4())+"@1-annum.com"
            fo.write(yearly_recur_ics(fixed[ferien],event_uuid,ferien))
        for ferien in moving:
            event_uuid = str(uuid.uuid4())+"@1-annum.com"
            fo.write(non_recur(moving[ferien]["dates"],event_uuid,ferien))
        fo.write(cal_footer)
    """
    
if __name__=="__main__":
    make_country_holiday("FR")
    make_country_holiday("GB")
    make_country_holiday("DE")
    make_country_holiday("JP")
