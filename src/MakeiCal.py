"""
Generic function for generation of .ics files
"""

import itertools
import uuid

vcal_header="""BEGIN:VCALENDAR
VERSION:2.0
PRODID:1-annum
"""

vcal_footer = "END:VCALENDAR"

vevent_rdate_template = """BEGIN:VEVENT
UID:%s
DTSTART;VALUE=DATE:%s
DTEND;VALUE=DATE:%s
RDATE;VALUE=DATE:%s
DTSTAMP:20210101T170000Z
ORGANIZER;CN=Auberon Vacher:MAILTO:contact@1-annum.com
SUMMARY:%s
END:VEVENT
"""

vevent_rrule_template="""BEGIN:VEVENT
UID:%s
DTSTART;VALUE=DATE:%s
DTEND;VALUE=DATE:%s
RRULE:%s
DTSTAMP:20210101T170000Z
ORGANIZER;CN=Auberon Vacher:MAILTO:contact@1-annum.com
SUMMARY: %s 
END:VEVENT
"""

def get_rrule_vevent(date,rrule,summary):
    event_uuid = str(uuid.uuid4())+"@1-annum.com"
    #dstart=date.strftime("%Y%m%dT%H%m%SZ")
    dstart=date.strftime("%Y%m%d")
    res = vevent_rrule_template%(event_uuid,dstart,dstart,rrule,summary)
    return res

def get_rdate_vevent(dates,summary):
    event_uuid = str(uuid.uuid4())+"@1-annum.com"
    def mygrouper(n, iterable):
        args = [iter(iterable)] * n
        return ([e for e in t if e != None] for t in itertools.zip_longest(*args))
    #dates = [d.strftime("%Y%m%dT%H%m%SZ") for d in dates]
    dates = [d.strftime("%Y%m%d") for d in dates]
    dte = dates[0]
    dts = dates[0]
    dates = list(mygrouper(3,dates))
    str_dates = []
    for d in dates:
        str_dates.append(",".join(d))
    rdates=",\n ".join(str_dates)
    res=vevent_rdate_template%(event_uuid,dte,dts,rdates,summary)
    return res
    
def write_ical(fn,rrules,rdates):
    with open(fn,"w",encoding='utf-8') as fo:
        fo.write(vcal_header)
        for doi in rrules:
            event_uuid = str(uuid.uuid4())+"@1-annum.com"
            #get_rrule_vevent(date,rrule,summary)
            vevent = get_rrule_vevent(rrules[doi]["dtstart"],rrules[doi]["rrule"],doi)
            fo.write(vevent)
        for doi in rdates:
            event_uuid = str(uuid.uuid4())+"@1-annum.com"
            #get_rdate_vevent(dates,summary)
            try:
                vevent = get_rdate_vevent(rdates[doi],doi)
            except:
                print(73,doi,rdates[doi])
                raise
            fo.write(vevent)
        fo.write(vcal_footer)
    print(f"succesfully saved {fn}")