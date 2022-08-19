# -*- coding: utf-8 -*-
"""
This module offers a generic easter computing method for any given year, using
Western, Orthodox or Julian algorithms.
"""

import datetime
import itertools
import uuid

from MakeiCal import write_ical

__all__ = ["easter", "EASTER_JULIAN", "EASTER_ORTHODOX", "EASTER_WESTERN"]

EASTER_JULIAN = 1
EASTER_ORTHODOX = 2
EASTER_WESTERN = 3


def easter(year, method=EASTER_WESTERN):
    """
    This method was ported from the work done by GM Arts,
    on top of the algorithm by Claus Tondering, which was
    based in part on the algorithm of Ouding (1940), as
    quoted in "Explanatory Supplement to the Astronomical
    Almanac", P.  Kenneth Seidelmann, editor.

    This algorithm implements three different easter
    calculation methods:

    1 - Original calculation in Julian calendar, valid in
        dates after 326 AD
    2 - Original method, with date converted to Gregorian
        calendar, valid in years 1583 to 4099
    3 - Revised method, in Gregorian calendar, valid in
        years 1583 to 4099 as well

    These methods are represented by the constants:

    * ``EASTER_JULIAN   = 1``
    * ``EASTER_ORTHODOX = 2``
    * ``EASTER_WESTERN  = 3``

    The default method is method 3.

    More about the algorithm may be found at:

    `GM Arts: Easter Algorithms <http://www.gmarts.org/index.php?go=415>`_

    and

    `The Calendar FAQ: Easter <https://www.tondering.dk/claus/cal/easter.php>`_

    """

    if not (1 <= method <= 3):
        raise ValueError("invalid method")

    # g - Golden year - 1
    # c - Century
    # h - (23 - Epact) mod 30
    # i - Number of days from March 21 to Paschal Full Moon
    # j - Weekday for PFM (0=Sunday, etc)
    # p - Number of days from March 21 to Sunday on or before PFM
    #     (-6 to 28 methods 1 & 3, to 56 for method 2)
    # e - Extra days to add for method 2 (converting Julian
    #     date to Gregorian date)

    y = year
    g = y % 19
    e = 0
    if method < 3:
        # Old method
        i = (19*g + 15) % 30
        j = (y + y//4 + i) % 7
        if method == 2:
            # Extra dates to convert Julian to Gregorian date
            e = 10
            if y > 1600:
                e = e + y//100 - 16 - (y//100 - 16)//4
    else:
        # New method
        c = y//100
        h = (c - c//4 - (8*c + 13)//25 + 19*g + 15) % 30
        i = h - (h//28)*(1 - (h//28)*(29//(h + 1))*((21 - g)//11))
        j = (y + y//4 + i + 2 - c + c//4) % 7

    # p can be from -6 to 56 corresponding to dates 22 March to 23 May
    # (later dates apply to method 2, although 23 May never actually occurs)
    p = i - j + e
    d = 1 + (p + 27 + (p + 6)//40) % 31
    m = 3 + (p + 26)//30
    return datetime.date(int(y), int(m), int(d))
    
def get_moving_feasts(start_year=2000,end_year=2040):
    easters = []
    ash_weds = []
    pentecosts = []
    for y in range(start_year,end_year+1):

        easter_day = easter(y)
        ash_wednesday = easter_day+datetime.timedelta(days=-46)
        pentecost_day = easter_day+datetime.timedelta(days=49)
        easters.append(easter_day)
        ash_weds.append(ash_wednesday)
        pentecosts.append(pentecost_day)
    return easters,ash_weds, pentecosts
    
def mygrouper2(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))
    
def make_ical2(lang="fr",start_year=2000,end_year=2040):
    easters,ash_weds, pentecosts = get_moving_feasts()
    moving_feasts = {"easter":{"dates":easters,"fr":"Pâques","en":"Easter","de":"Ostern"},
                 "pentecosts":{"dates":pentecosts,"fr":"Pâques","en":"Easter","de":"Ostern"},
                 "ash":{"dates":ash_weds,"fr":"Mercredi des Cendres","en":"Ash Wednesday","de":"Aschermittwoch"}
                 }
    with open("catho_%s_%s_%s.ics"%(start_year,end_year,lang),"w") as fo:
        fo.write(catho_ical_fixed)
        for moving in moving_feasts:
            event_uuid = str(uuid.uuid4())+"@1-annum.com"
            dates = [d.strftime("%Y%m%dT%H%m%SZ") for d in moving_feasts[moving]["dates"]]
            dts = dates[0]
            dte = dates[0]
            #TODO: since ical lines must be <75 characters - splitting every 4 dates
            dates = list(mygrouper(3,dates))
            str_dates = []
            for d in dates:
                str_dates.append(",".join(d))
            dates="\n ".join(str_dates)
            description = moving_feasts[moving][lang]
            fo.write(moving_header%(event_uuid,dte,dts,dates,description))
        fo.write("END:VCALENDAR")

    
def get_first_advent(year):
    """ Advent Sunday is the fourth Sunday before Christmas Day. """
    xmas_m1 = datetime.date(year,12,24)
    sundays_count = 0
    for i in range(28):
        day = xmas_m1 + datetime.timedelta(days=-i)
        if day.weekday() ==6: # MON = 0, SUN = 6
            sundays_count+=1
            if sundays_count==4:
                return day
    
def get_first_advents(year_start=2000,year_end=2040):
    first_advents = []
    for y in range(year_start,year_end+1):
        first_advents.append(get_first_advent(y))
    return first_advents

def make_catho(year_start=2000,year_end=2040):
     
    easters, ash_weds, pentecosts = get_moving_feasts(start_year=2000,end_year=2040)
    advents = get_first_advents(year_start=2000,year_end=2040)
    
    
    for lang in ["fr","en"]:
        feasts = {"Paques":{"fr":"Pâques","en":"Easter"},
                  "Mercredi des cendres":{"fr":"Mercredi des cendres","en":"Ash Wednesday"},
                  "Pentecote": {"fr":"Pentecôte","en":"Pentecost"},
                  "Avent": {"fr":"Avent","en":"Advent"},
                  "Epiphanie": {"fr":"Epiphanie","en":"Epiphanie"},
                  "Presentation de Jésus au Temple": {"fr":"Présentation de Jésus au Temple","en":"Presentation Jesus"},
                  "St Joseph": {"fr": "St Joseph", "en":"St Joseph"},
                  "Annonciation":{"fr":"Annonciation", "en":"Annonciation"},
                  "Saints Apotres Pierre et St Paul": {"fr": "Saints Apotres Pierre et St Paul", 
                                                       "en": "Saints Apotres Pierre et St Paul"},
                  "Assomption": {"fr":"Assomption","en":"Assomption"},
                  "Toussaint": {"fr":"Toussaint","en":"All saints"},
                  "Immaculee Conception": {"fr":"Immaculée Conception","en":"Immaculate Conception"},
                  "Vigile de Noel": {"fr":"Vigile de Noël","en":"Christmas eve"},
                  "Noel": {"fr":"Noël","en":"Christmas"},
                }
        rdates = {feasts["Paques"][lang]: easters,\
                  feasts["Mercredi des cendres"][lang]: ash_weds,\
                  feasts["Pentecote"][lang]: pentecosts,\
                  feasts["Avent"][lang]: advents
             }
        rrules = {feasts["Epiphanie"][lang]:{"dtstart":datetime.date(2000,1,6),"rrule":"FREQ=YEARLY;"},\
                  feasts["Presentation de Jésus au Temple"][lang]:{"dtstart":datetime.date(2000,2,2),"rrule":"FREQ=YEARLY;"},\
                  feasts["St Joseph"][lang]:{"dtstart":datetime.date(2000,3,19),"rrule":"FREQ=YEARLY;"},\
                  feasts["Annonciation"][lang] : {"dtstart":datetime.date(2000,3,25),"rrule":"FREQ=YEARLY;"},\
                  feasts["Saints Apotres Pierre et St Paul"][lang] : {"dtstart":datetime.date(2000,6,29),"rrule":"FREQ=YEARLY;"},\
                  feasts["Assomption"][lang] : {"dtstart":datetime.date(2000,8,15),"rrule":"FREQ=YEARLY;"},\
                  feasts["Toussaint"][lang] : {"dtstart":datetime.date(2000,11,1),"rrule":"FREQ=YEARLY;"},\
                  feasts["Immaculee Conception"][lang] : {"dtstart":datetime.date(2000,12,8),"rrule":"FREQ=YEARLY;"},\
                  feasts["Vigile de Noel"][lang] : {"dtstart":datetime.date(2000,12,24),"rrule":"FREQ=YEARLY;"},\
                  feasts["Noel"][lang] : {"dtstart":datetime.date(2000,12,25),"rrule":"FREQ=YEARLY;"}
                  }
        write_ical(f"catho_{year_start}_{year_end}_{lang}.ics",rrules,rdates)

if __name__=="__main__":
    make_catho()