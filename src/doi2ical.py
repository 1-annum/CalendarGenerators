""" FR- DOI
"""

import datetime
import uuid

from catho2ical import easter,get_first_advent

from MakeiCal import vcal_header,get_rrule_vevent,get_rdate_vevent,vcal_footer,write_ical

def get_mothers_days_fr(year_start,year_end):
    """
    La date est variable, chaque année elle a lieu le dernier dimanche de mai, 
    sauf si celui-ci coïncide avec la Pentecôte. Dans ce cas, la Fête des Mères 
    est décalée au premier dimanche de juin.
    """
    mothers_day = []
    for y in range(year_start,year_end+1):
        easter_day=easter(y)
        pentecost_day = easter_day+datetime.timedelta(days=49)
        idx = (pentecost_day.weekday() + 1) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
        if pentecost_day.month==5 and pentecost_day.day>24:
            mothers_day.append(pentecost_day+datetime.timedelta(days=7))
        else:
            for i in range(0,7):
                last_week_may_day = datetime.date(y,5,31-i)
                idx= last_week_may_day.weekday()
                if idx==6:
                    mothers_day.append(last_week_may_day)
    return mothers_day

def get_vattertags_de(year_start,year_end):
    """ Christi Himmelfahrt also 39 Tage nach dem Ostersonntag gefeiert.
    Der volkstümliche Vatertag wird in Deutschland an Christi Himmelfahrt begangen,
    dem 40. Tag des Osterfestkreises.
    """
    vatertags = []
    for y in range(year_start,year_end+1):
        easter_day=easter(y)
        vatertags.append(easter_day+datetime.timedelta(days=49))
    return vatertags

def get_oktoberfest(year_start,year_end):
    """
    Eröffnet wird seither am Samstag nach dem 15. September, 
    Ende des Festes ist traditionell der erste Sonntag im Oktober. 
    """
    oktoberfest_tags = []
    for y in range(year_start,year_end+1):
        for dom in range(16,23):
            oktoberfest_tag=datetime.date(y,9,dom)
            idx = oktoberfest_tag.weekday() # MON = 0, SUN = 6
            if idx==5:
                oktoberfest_tags.append(oktoberfest_tag)
                break
    return oktoberfest_tags

def get_volkstreuer_tags(year_start=2000,year_end=2040):
    """
    https://de.wikipedia.org/wiki/Volkstrauertag

Der Volkstrauertag ist in Deutschland ein staatlicher Gedenktag und gehört zu den sogenannten stillen Tagen.
Er wird seit 1952 zwei Sonntage vor dem ersten Adventssonntag
    """
    volkstreuer_tags = []
    for y in range(year_start,year_end+1):
        first_advent = get_first_advent(y)
        volkstreuer_tags.append(first_advent+datetime.timedelta(days=-14))
    return volkstreuer_tags
    

def get_debut_soldes(year_start,year_end):
    """
    https://www.economie.gouv.fr/dgccrf/consommation/Pratiques-commerciales/Soldes
    
    Dates des soldes d'hiver et d'été 2020
    En application de l'article D. 310-15-2 du Code de commerce :
    les soldes d'hiver débutent le deuxième mercredi du mois de janvier à 8 heures du matin ; 
        cette date est avancée au premier mercredi du mois de janvier lorsque le deuxième mercredi 
        intervient après le 12 du mois ;
    les soldes d'été débutent le dernier mercredi du mois de juin à 8 heures du matin ; 
        cette date est avancée à l'avant-dernier mercredi du mois de juin lorsque le dernier mercredi 
        intervient après le 28 du mois.
    """
    debut_soldes = []
    prev_wed = None
    for y in range(year_start,year_end+1):
        for dom in range(1,15):
            day = datetime.date(y,1,dom)
            idx=day.weekday()
            if idx == 2:
                if dom<=5:
                    debut_soldes.append(day+datetime.timedelta(days=7))
                else:
                    debut_soldes.append(day)
                break
        for dom in range(30,23,-1):
            day =datetime.date(y,6,dom)
            idx=day.weekday()
            if idx == 2:
                if dom>28:
                    debut_soldes.append(day+datetime.timedelta(days=-7))
                else:
                    debut_soldes.append(day)
                break
    return debut_soldes
        

def make_fr(year_start=2000,year_end=2040):
    mothers_days = get_mothers_days_fr(year_start=2000,year_end=2040)
    soldes = get_debut_soldes(year_start=2000,year_end=2040)
    rdates = {"Fête des Mères": mothers_days,\
              "Ouverture soldes": soldes
             }
    
    rrules = {"Chandeleur":{"dtstart":datetime.date(2000,2,2),"rrule":"FREQ=YEARLY;"},\
            "Fête des pères": {"dtstart": datetime.date(2000,6,3),"rrule":"FREQ=YEARLY;"},\
            "Fête de la musique":{"dtstart": datetime.date(2000,6,21),"rrule":"FREQ=YEARLY;"},\
            "Journée du patrimoine":{"dtstart":datetime.date(2000,9,17),"rrule":"FREQ=YEARLY;INTERVAL=1;BYDAY=3SU;BYMONTH=6"}
            }
    write_ical("FR_doi_%s_%s.ics"%(year_start,year_end),rrules,rdates)
    
def make_de(year_start=2000,year_end=2040):
    vatertags = get_vattertags_de(year_start=2000,year_end=2040)
    oktoberfest_tags = get_oktoberfest(year_start=2000,year_end=2040)
    volkstreuer_tags = get_volkstreuer_tags(year_start=2000,year_end=2040)
    
    rrules = {"Muttertag":{"dtstart":datetime.date(2000,5,14),"rrule":"FREQ=YEARLY;BYMONTH=5;BYDAY=2SU"},\
              "Martinstag":{"dtstart":datetime.date(2000,1,11),"rrule":"FREQ=YEARLY;"},\
              "Nikolaus":{"dtstart":datetime.date(2000,12,6),"rrule":"FREQ=YEARLY;"}
             }
    rdates = {"Vatertags":vatertags,\
              "Oktober Fest": oktoberfest_tags,\
              "VolksTreuer": volkstreuer_tags,
            }
    write_ical("DE_doi_%s_%s.ics"%(year_start,year_end),rrules,rdates)

if __name__=="__main__":
    make_fr(year_start=2000,year_end=2040)
    make_de(year_start=2000,year_end=2040)